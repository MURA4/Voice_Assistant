import os
import traceback

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
        self.mpcHcPath = ""
        self.mpcIsUse = False
        self.mpcIsUseHttpRemote = False

        self.isOnline = False
        self.version = version

        self.voiceAssNames = []

        self.ttsEngineId = ""

        self.logPolicy = ""

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
        self.ttss[self.ttsEngineId][1](self,text_to_speech)

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
                        next_context = context[keyall]
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



