import os
import traceback
from threading import Timer
import time

import sounddevice as sound_device
import soundfile as sound_file

from jaa import JaaCore

version = "2.1"

class VACore(JaaCore):
    def __init__(self):
        JaaCore.__init__(self)

        self.timers = [-1,-1,-1,-1,-1,-1,-1,-1]
        self.timersFuncUpd = [None,None,None,None,None,None,None,None]
        self.timersFuncEnd = [None,None,None,None,None,None,None,None]
        self.timersDuration = [0,0,0,0,0,0,0,0]

        self.commands = {
        }

        self.ttss = {
        }

        # more options
        self.contextRemoteWaitForCall = False
        self.mpcHcPath = ""
        self.mpcIsUse = False
        self.mpcIsUseHttpRemote = False
        self.remoteTTS = "none"
        self.remoteTTSResult = None
        self.isOnline = False
        self.version = version

        self.voiceAssNames = []

        self.ttsEngineId = ""

        self.logPolicy = ""
        
        self.contextTimer = None
        self.contextTimerLastDuration = 0

        import mpcapi.core
        self.mpchc = mpcapi.core.MpcAPI()

    def init_with_plugins(self):
        self.init_plugins(["core"])
        if self.isOnline:
            print("VoiceAssistantCore v{0}: run online".format(version))
        else:
            print("VoiceAssistantCore v{0}: run OFFLINE".format(version))
        print("TTS engines: ",self.ttss.keys())
        print("Commands list: ",self.commands.keys())
        print("Assistant names: ",self.voiceAssNames)

        self.setup_assistant_voice()

    # ----------- process plugins functions ------
    def process_plugin_manifest(self,modname,manifest): #не используется
        # is req online?
        plugin_req_online = True
        if "require_online" in manifest:
            plugin_req_online = manifest["require_online"]

        # adding commands from plugin manifest
        if "commands" in manifest: # process commands
            for cmd in manifest["commands"].keys():
                if not self.isOnline and plugin_req_online:
                    # special processing
                    self.commands[cmd] = self.stub_online_required
                else:
                    # normal add command
                    self.commands[cmd] = manifest["commands"][cmd]

        # adding tts engines from plugin manifest
        if "tts" in manifest: # process commands
            for cmd in manifest["tts"].keys():
                self.ttss[cmd] = manifest["tts"][cmd]

    def stub_online_required(self,core,phrase):
        self.play_voice_assistant_speech("Для этой команды необходим онлайн")

    # ----------- text-to-speech functions ------

    def setup_assistant_voice(self): #не используется
        self.ttss[self.ttsEngineId][0](self)

    def play_voice_assistant_speech(self,text_to_speech:str):
        self.lastSay = text_to_speech
        remoteTTSList = self.remoteTTS.split(",")

        self.remoteTTSResult = {}
        is_processed = False
        if "none" in remoteTTSList: # no remote tts, do locally anything
            #self.remoteTTSResult = "" # anywhere, set it ""

            if self.ttss[self.ttsEngineId][1] != None:
                self.ttss[self.ttsEngineId][1](self,text_to_speech)
            else:
                if self.useTTSCache:
                    tts_file = self.get_tts_cache_file(text_to_speech)
                else:
                    tts_file = self.get_tempfilename()+".wav"

                #print('Temp TTS filename: ', tts_file)
                if not self.useTTSCache or self.useTTSCache and not os.path.exists(tts_file):
                    self.tts_to_filewav(text_to_speech, tts_file)

                self.play_wav(tts_file)
                if not self.useTTSCache and os.path.exists(tts_file):
                    os.unlink(tts_file)

            is_processed = True

        if "saytxt" in remoteTTSList: # return only last say txt
            self.remoteTTSResult["restxt"] = text_to_speech

            is_processed = True

        if "saywav" in remoteTTSList:
            if self.useTTSCache:
                tts_file = self.get_tts_cache_file(text_to_speech)
            else:
                tts_file = self.get_tempfilename()+".wav"

            if not self.useTTSCache or self.useTTSCache and not os.path.exists(tts_file):
                self.tts_to_filewav(text_to_speech, tts_file)
            #self.play_wav(tts_file)
            import base64

            with open(tts_file, "rb") as wav_file:
                encoded_string = base64.b64encode(wav_file.read())

            if not self.useTTSCache and os.path.exists(tts_file):
                os.unlink(tts_file)

            self.remoteTTSResult["wav_base64"] = encoded_string

            is_processed = True

        if not is_processed:
            print("Ошибка при выводе TTS - remoteTTS не был обработан.")
            print("Текущий remoteTTS: {}".format(self.remoteTTS))
            print("Текущий remoteTTSList: {}".format(remoteTTSList))
            print("Ожидаемый remoteTTS (например): 'none'")



        
    def context_set(self,context,duration = None):
        if duration == None:
            duration = self.contextDefaultDuration

        self.context_clear()

        self.context = context
        self.contextTimerLastDuration = duration
        self.contextTimer = Timer(duration,self._context_clear_timer)

        remoteTTSList = self.remoteTTS.split(",")
        if self.contextRemoteWaitForCall and ("saytxt" in remoteTTSList or "saywav" in remoteTTSList):
            pass # wait for run context timer
        else:
            self.contextTimer.start()
            
        #def _timer_context
    def _context_clear_timer(self):
        print("Context cleared after timeout")
        self.contextTimer = None
        self.context_clear()

    def context_clear(self):
        self.context = None
        if self.contextTimer != None:
            self.contextTimer.cancel()
            self.contextTimer = None

    def say(self,text_to_speech:str): # alias for play_voice_assistant_speech
        self.play_voice_assistant_speech(text_to_speech)


    # -------- основная функция ----------

    def execute_next(self,command,context):
        if context == None:
            context = self.commands

        if isinstance(context,dict):
            pass
        else:
            # it is function to call!
            #context(self,command)
            self.call_ext_func_phrase(command,context)
            return

        try:
            for keyall in context.keys():
                keys = keyall.split("|")
                for key in keys:
                    if command.startswith(key):
                        rest_phrase = command[(len(key)+1):]
                        next_context = context[keyall] #здесь вызывается то, что лежит по ключу keyall
                        self.execute_next(rest_phrase,next_context)
                        #print(next_context)
                        #print(rest_phrase)

                        #if isinstance(next_context,dict):


                        #commands[key](*args)
                        #print
                        return
                    else:
                        #print("Command not found", command_name)
                        #play_voice_assistant_speech("Извини, я не поняла")
                        pass

            # if not founded
            self.play_voice_assistant_speech("Извини, я не поняла")
        except Exception as err:
            print(traceback.format_exc())

    # ----------- таймеры -----------
    def set_timer(self, duration, timerFuncEnd, timerFuncUpd = None):
        # print "Start set_timer!"
        curtime = time.time()
        for i in range(len(self.timers)):
            if self.timers[i] <= 0:
                # print "Found timer!"
                self.timers[i] = curtime+duration  #duration
                self.timersFuncEnd[i] = timerFuncEnd
                print("New Timer ID =", str(i), ' curtime=', curtime, 'duration=', duration, 'endtime=', self.timers[i])
                return i
        return -1  # no more timer valid

    def clear_timer(self, index, runEndFunc=False):
        if runEndFunc and self.timersFuncEnd[index] != None:
            self.call_ext_func(self.timersFuncEnd[index])
        self.timers[index] = -1
        self.timersDuration[index] = 0
        self.timersFuncEnd[index] = None

    def clear_timers(self): # not calling end function
        for i in range(len(self.timers)):
            if self.timers[i] >= 0:
                self.timers[i] = -1
                self.timersFuncEnd[i] = None

    def _update_timers(self):
        curtime = time.time()
        for i in range(len(self.timers)):
            if(self.timers[i] > 0):
                if curtime >= self.timers[i]:
                    print("End Timer ID =", str(i), ' curtime=', curtime, 'endtime=', self.timers[i])
                    self.clear_timer(i,True)

    # --------- calling functions -----------

    def call_ext_func(self,funcparam):
        if isinstance(funcparam,tuple): # funcparam =(func, param)
            funcparam[0](self,funcparam[1])
        else: # funcparam = func
            funcparam(self)

    def call_ext_func_phrase(self,phrase,funcparam):
        if isinstance(funcparam,tuple): # funcparam =(func, param)
            funcparam[0](self,phrase,funcparam[1])
        else: # funcparam = func
            funcparam(self,phrase)

    # ------- play wav from subfolder ----------
    def play_wav(self,wavfile):
        filename = os.path.dirname(__file__)+"/"+wavfile

        #filename = 'timer/Sounds/Loud beep.wav'
        # now, Extract the data and sampling rate from file
        data_set, fsample = sound_file.read(filename, dtype = 'float32')
        sound_device.play(data_set, fsample)
        # Wait until file is done playing
        status = sound_device.wait()



# ------------- команды и их обработка ---------------



