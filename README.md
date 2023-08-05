### What is Lakul?
This is a project I have made built around [OpenAI Whisper](https://openai.com/blog/whisper/) 
speech recognition engine.

This should work on both Windows x86_64 and Linux x86_64 and Raspberry Pi (tested on a Pi 4 and a Pi Zero 2 W running 64 Bit RPi OS).

It is called Lakul based off of the Star Trek ship, [The SS Lakul](https://memory-alpha.fandom.com/wiki/SS_Lakul).

I made this because integrating TensorflowASR (like in [Soran](https://github.com/LordofBone/soran)) was slow and clunky
or Mozilla Deepspeech like in [Guinan](https://github.com/LordofBone/guinan) didn't work on RPi.

##### What is Whisper?
Whisper is a speech recognition engine from [OpenAI](https://github.com/openai/whisper).

It allows for local (offline) speech recognition, so you don't have to connect to an online API to perform decent 
speech recognition.

I have made this so that I can integrate into other projects such as my upcoming T-800 project. My previous projects 
[Nvidianator](https://www.hackster.io/314reactor/the-nvidianator-341f7a) and 
[EDITH glasses](https://www.hackster.io/314reactor/e-d-i-t-h-glasses-5604fa) used 
[wit.ai](https://wit.ai/) to perform speech recognition; which is effective; but of course requires API keys and
internet access.

##### Integrating Lakul into a project
If you want to integrate Lakul into another system, such as a robot - you can pull down the repo into the folder of
the project you are working on as a submodule.

`git submodule add https://github.com/LordofBone/Lakul.git`

Install the requirements with:
`pip install -r requirements.txt`

If the Whisper install doesn't work from requirements.txt, you can install it manually with:
`pip install git+https://github.com/openai/whisper.git`

and to update it:
`pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git`

If you are running on RPi you will need to ensure that the pytorch version is at 1.12.0, or you will get an illegal instruction error.

Next you need to copy the file `config/whisper_config_template.py` into a file called `config/whisper_config.py` and 
add your own API key from [OpenAI](https://platform.openai.com/); if you wish to use the online version (will be considerably
faster on a RPi 4 than the offline version, but of course will cost you money per inference).

You can then switch between local and online versions by changing the `offline_mode` variable in `config/whisper_config.py`.

You can also change the model size of the local version by changing the model_size variable in config/whisper_config.py.

The available_models are = ["tiny", "base", "small", "medium", "large"]

Importing SpeechInference from integrate_stt.py as a submodule into another project:
`from Lakul.integrate_stt import SpeechtoTextHandler`
Which can then be called from the program to record audio and get the text output.
`SpeechtoText = SpeechtoTextHandler()`
`SpeechtoText.initiate_recording()`
`print(SpeechtoText.run_inference())`

Also, the status of listening inferencing can be obtained from the class:
`print(SpeechtoTextTest.inferencing)`
`print(SpeechtoTextTest.listening)`