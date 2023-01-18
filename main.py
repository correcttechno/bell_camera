import agorartc
import ctypes
import wave

audio_data = b''
channel = -1
samplewidth = -1
framerate = -1


class MyRtcEngineEventHandler(agorartc.RtcEngineEventHandlerBase):

    def __init__(self, rtc):
        super().__init__()
        self.rtc = rtc

    def onWarning(self, warn, msg):
        print("warn: ")
        print(warn)

    def onError(self, err, msg):
        print("err: ")
        print(err)

    def onJoinChannelSuccess(self, channel, uid, elapsed):
        print("onJoinChannelSuccess")

    def onRejoinChannelSuccess(self, channel, uid, elapsed):
        print("onRejoinChannelSuccess")

    def onLeaveChannel(self, stats):
        print("onLeaveChannel")

    def onClientRoleChanged(self, oldRole, newRole):
        print("onClientRoleChanged")

    def onUserJoined(self, uid, elapsed):
        print("onUserJoined")

    def onUserOffline(self, uid, reason):
        print("onUserOffline")

    def onLastmileQuality(self, quality):
        print("onLastmileQuality")

    def onLastmileProbeResult(self, res):
        print("onLastmileProbeResult")

    def onConnectionInterrupted(self):
        print("onConnectionInterrupted")

    def onConnectionLost(self):
        print("onConnectionLost")

    def onConnectionBanned(self):
        print("onConnectionBanned")

    def onApiCallExecuted(self, err, api, res):
        print("onApiCallExecuted" + str(api))

    def onRequestToken(self):
        print("onRequestToken")

    def onTokenPrivilegeWillExpire(self, token):
        print("onTokenPrivilegeWillExpire")

    def onAudioQuality(self, uid, quality, delay, lost):
        print("onAudioQuality")

    def onRtcStats(self, stats):
        print("onRtcStats")

    def onNetworkQuality(self, uid, txQuality, rxQuality):
        print("onNetworkQuality")

    def onLocalVideoStats(self, stats):
        print("onLocalVideoStats")

    def onRemoteVideoStats(self, stats):
        print("onRemoteVideoStats")

    def onLocalAudioStats(self, stats):
        print("onLocalAudioStats")

    def onRemoteAudioStats(self, stats):
        print("onRemoteAudioStats")

    def onLocalAudioStateChanged(self, state, error):
        print("onLocalAudioStateChanged")

    def onRemoteAudioStateChanged(self, uid, state, reason, elapsed):
        print("onRemoteAudioStateChanged")

    def onAudioVolumeIndication(self, speakers, speakerNumber, totalVolume):
        print("onAudioVolumeIndication")

    def onActiveSpeaker(self, uid):
        print("onActiveSpeaker")

    def onVideoStopped(self):
        print("onVideoStopped")

    def onFirstLocalVideoFrame(self, width, height, elapsed):
        print("onFirstLocalVideoFrame")

    def onFirstRemoteVideoDecoded(self, uid, width, height, elapsed):
        print("onFirstRemoteVideoDecoded")

    def onFirstRemoteVideoFrame(self, uid, width, height, elapsed):
        print("onFirstRemoteVideoFrame")

    def onUserMuteAudio(self, uid, muted):
        print("onUserMuteAudio")

    def onUserMuteVideo(self, uid, muted):
        print("onUserMuteVideo")

    def onUserEnableVideo(self, uid, enabled):
        print("onUserEnableVideo")

    def onAudioDeviceStateChanged(self, deviceId, deviceType, deviceState):
        print("onAudioDeviceStateChanged")

    def onAudioDeviceVolumeChanged(self, deviceType, volume, muted):
        print("onAudioDeviceVolumeChanged")

    def onCameraReady(self):
        print("onCameraReady")

    def onCameraFocusAreaChanged(self, x, y, width, height):
        print("onCameraFocusAreaChanged")

    def onCameraExposureAreaChanged(self, x, y, width, height):
        print("onCameraExposureAreaChanged")

    def onAudioMixingFinished(self):
        print("onAudioMixingFinished")

    def onAudioMixingStateChanged(self, state, errorCode):
        print("onAudioMixingStateChanged")

    def onRemoteAudioMixingBegin(self):
        print("onRemoteAudioMixingBegin")

    def onRemoteAudioMixingEnd(self):
        print("onRemoteAudioMixingEnd")

    def onAudioEffectFinished(self, soundId):
        print("onAudioEffectFinished")

    def onFirstRemoteAudioDecoded(self, uid, elapsed):
        print("onFirstRemoteAudioDecoded")

    def onVideoDeviceStateChanged(self, deviceId, deviceType, deviceState):
        print("onVideoDeviceStateChanged")

    def onLocalVideoStateChanged(self, localVideoState, error):
        print("onLocalVideoStateChanged")

    def onVideoSizeChanged(self, uid, width, height, rotation):
        print("onVideoSizeChanged")

    def onRemoteVideoStateChanged(self, uid, state, reason, elapsed):
        print("onRemoteVideoStateChanged")

    def onUserEnableLocalVideo(self, uid, enabled):
        print("onUserEnableLocalVideo")

    def onStreamMessage(self, uid, streamId, data, length):
        print("onStreamMessage")

    def onStreamMessageError(self, uid, streamId, code, missed, cached):
        print("onStreamMessageError")

    def onMediaEngineLoadSuccess(self):
        print("onMediaEngineLoadSuccess")

    def onMediaEngineStartCallSuccess(self):
        print("onMediaEngineStartCallSuccess")

    def onChannelMediaRelayStateChanged(self, state, code):
        print("onChannelMediaRelayStateChanged")

    def onChannelMediaRelayEvent(self, code):
        print("onChannelMediaRelayEvent")

    def onFirstLocalAudioFrame(self, elapsed):
        print("onFirstLocalAudioFrame")

    def onFirstRemoteAudioFrame(self, uid, elapsed):
        print("onFirstRemoteAudioFrame")

    def onRtmpStreamingStateChanged(self, url, state, errCode):
        print("onRtmpStreamingStateChanged")

    def onStreamPublished(self, url, error):
        print("onStreamPublished")

    def onStreamUnpublished(self, url):
        print("onStreamUnpublished")

    def onTranscodingUpdated(self):
        print("onTranscodingUpdated")

    def onStreamInjectedStatus(self, url, uid, status):
        print("onStreamInjectedStatus")

    def onAudioRouteChanged(self, routing):
        print("onAudioRouteChanged")

    def onLocalPublishFallbackToAudioOnly(self, isFallbackOrRecover):
        print("onLocalPublishFallbackToAudioOnly")

    def onRemoteSubscribeFallbackToAudioOnly(self, uid, isFallbackOrRecover):
        print("onRemoteSubscribeFallbackToAudioOnly")

    def onRemoteAudioTransportStats(self, uid, delay, lost, rxKBitRate):
        print("onRemoteAudioTransportStats")

    def onRemoteVideoTransportStats(self, uid, delay, lost, rxKBitRate):
        print("onRemoteVideoTransportStats")

    def onMicrophoneEnabled(self, enabled):
        print("onMicrophoneEnabled")

    def onConnectionStateChanged(self, state, reason):
        print("onConnectionStateChanged")

    def onNetworkTypeChanged(self, type):
        print("onNetworkTypeChanged")

    def onLocalUserRegistered(self, uid, userAccount):
        print("onLocalUserRegistered")

    def onUserInfoUpdated(self, uid, info):
        print("onUserInfoUpdated")


class MyAudioFrameObserver(agorartc.AudioFrameObserver):
    def onRecordAudioFrame(self, type1, samples, bytesPerSample, channels, samplesPerSec, buffer1, renderTimeMs, avsync_type):
        pass

    def onPlaybackAudioFrame(self, type1, samples, bytesPerSample, channels, samplesPerSec, buffer1, renderTimeMs, avsync_type):
        pass

    def onMixedAudioFrame(self, type1, samples, bytesPerSample, channels, samplesPerSec, buffer1, renderTimeMs, avsync_type):
        print(">>>>>>>> Input any character to stop audio capture and save audio data into a wave file.")
        print("onMixedAudioFrame: type {}, samples {}, bytesPerSample {}, channels {}, samplesPerSec {}, buffer {}, renderTimeMs {}, avsync_type {}".format(\
                                                 type1, samples, bytesPerSample, channels, samplesPerSec, buffer1, renderTimeMs, avsync_type))
        global audio_data, channel, samplewidth, framerate
        if channel == -1:
            channel = channels
        if samplewidth == -1:
            samplewidth = bytesPerSample
        if framerate == -1:
            framerate = samplesPerSec

        audio_array = (ctypes.c_ubyte * samples * bytesPerSample * channels).from_address(buffer1)
        audio_data += bytes(audio_array)

    def onPlaybackAudioFrameBeforeMixing(self, uid, type1, samples, bytesPerSample, channels, samplesPerSec, buffer1, renderTimeMs, avsync_type):
        pass


rtc = agorartc.createRtcEngineBridge()
eventHandler = MyRtcEngineEventHandler(rtc)
rtc.initEventHandler(eventHandler)
# Please input your APP ID here.
rtc.initialize("a546d6650a5340588abc9fbc937d60d5", None, agorartc.AREA_CODE_GLOB & 0xFFFFFFFF)
afo = MyAudioFrameObserver()
rtc.joinChannel("007eJxTYFC+++NX+9GYV/4xDOwB7qopv5pDAuV6V3WwvLrX7m7x0FqBIdHUxCzFzMzUINHU2MTA1MIiMSnZMg2Ijc1TzAxSTAVyjic3BDIyBHxRZGVkYGRgAWIQnwlMMoNJFig7L7WcgQEAM7Ugog==", "new", "", 0)
rtc.startPreview()
rtc.enableVideo()
agorartc.registerAudioFrameObserver(rtc, afo)
input()  # Press any key to come to an end.
agorartc.unregisterAudioFrameObserver(rtc, afo)

# Save the audio data into a wave file.
if channel != -1 and samplewidth != -1 and framerate != -1:
    print(">>>>>>>> Start saving audio data.")
    with wave.open("sound.wav", "wb") as f:
        f.setnchannels(channel)
        f.setsampwidth(samplewidth)
        f.setframerate(framerate)
        f.writeframesraw(audio_data)

rtc.leaveChannel()
rtc.release()
