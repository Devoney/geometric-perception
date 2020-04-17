#include <chrono>
#include <stdio.h>
#include <stdlib.h>
#include <thread>

#include <windows.h> 
#include <stdio.h> 
#include <tchar.h>
#include <strsafe.h>

#define BUFSIZE 640 * 480 * sizeof(uint16_t)

#include <ST/CaptureSession.h>

HANDLE hPipe = INVALID_HANDLE_VALUE, hThread = NULL;
LPCTSTR lpszPipename = TEXT("\\\\.\\pipe\\occipital-structure-core");
DWORD cbWritten = 0;
const uint8_t *depthRGBA;
const uint16_t *depthInMillimeters;

struct SessionDelegate : ST::CaptureSessionDelegate {
    void captureSessionEventDidOccur(ST::CaptureSession *session, ST::CaptureSessionEventId event) override {
        printf("Received capture session event %d (%s)\n", (int)event, ST::CaptureSessionSample::toString(event));
        switch (event) {
            case ST::CaptureSessionEventId::Booting: break;
            case ST::CaptureSessionEventId::Connected:
                printf("Starting streams...\n");
                printf("Sensor Serial Number is %s \n ", session->sensorSerialNumber());
                session->startStreaming();
                break;
            case ST::CaptureSessionEventId::Disconnected:
            case ST::CaptureSessionEventId::Error:
                printf("Capture session error\n");
                exit(1);
                break;
            default:
                printf("Capture session event unhandled\n");
        }
    }

    void captureSessionDidOutputSample(ST::CaptureSession *, const ST::CaptureSessionSample& sample) override {
        printf("Received capture session sample of type %d (%s)\n", (int)sample.type, ST::CaptureSessionSample::toString(sample.type));
        switch (sample.type) {
            case ST::CaptureSessionSample::Type::DepthFrame:
                printf("Depth frame: size %dx%d\n", sample.depthFrame.width(), sample.depthFrame.height());				
                break;
            case ST::CaptureSessionSample::Type::VisibleFrame:
                printf("Visible frame: size %dx%d\n", sample.visibleFrame.width(), sample.visibleFrame.height());
                break;
            case ST::CaptureSessionSample::Type::InfraredFrame:
                printf("Infrared frame: size %dx%d\n", sample.infraredFrame.width(), sample.infraredFrame.height());
                break;
            case ST::CaptureSessionSample::Type::SynchronizedFrames:
                printf("Synchronized frames: depth %dx%d visible %dx%d infrared %dx%d\n", sample.depthFrame.width(), sample.depthFrame.height(), sample.visibleFrame.width(), sample.visibleFrame.height(), sample.infraredFrame.width(), sample.infraredFrame.height());
				if (sample.depthFrame.isValid()) {
					// sample.depthFrame.saveImageAsPointCloudMesh("test.ply");
					
					depthInMillimeters = sample.depthFrame.convertDepthToUShortInMillimeters();
					int nonZeroValueCount = 0;
					uint16_t value = 0;
					for (int i = 0; i < 480 * 640; i++)
					{
						value = depthInMillimeters[i];
						if (value != 0) {
							nonZeroValueCount++;
						}
					}
					BOOL fSuccess = WriteFile(
						hPipe,        // handle to pipe 
						depthInMillimeters,     // buffer to write from 
						BUFSIZE, // number of bytes to write 
						&cbWritten,   // number of bytes written 
						NULL);        // not overlapped I/O 

					// This worked 
					//depthRGBA = sample.depthFrame.convertDepthToRgba();
					//BOOL fSuccess = WriteFile(
					//	hPipe,        // handle to pipe 
					//	depthRGBA,     // buffer to write from 
					//	BUFSIZE, // number of bytes to write 
					//	&cbWritten,   // number of bytes written 
					//	NULL);        // not overlapped I/O 

					if (!fSuccess || BUFSIZE != cbWritten)
					{
						_tprintf(TEXT("WriteFile failed, GLE=%d.\n"), GetLastError());
					}
				}
                break;
            case ST::CaptureSessionSample::Type::AccelerometerEvent:
                printf("Accelerometer event: [% .5f % .5f % .5f]\n", sample.accelerometerEvent.acceleration().x, sample.accelerometerEvent.acceleration().y, sample.accelerometerEvent.acceleration().z);
                break;
            case ST::CaptureSessionSample::Type::GyroscopeEvent:
                printf("Gyroscope event: [% .5f % .5f % .5f]\n", sample.gyroscopeEvent.rotationRate().x, sample.gyroscopeEvent.rotationRate().y, sample.gyroscopeEvent.rotationRate().z);
                break;
            default:
                printf("Sample type unhandled\n");
        }
    }
};

int CreatePipe()
{
	_tprintf(TEXT("\nPipe Server: awaiting client connection on %s\n"), lpszPipename);
	hPipe = CreateNamedPipe(
		lpszPipename,             // pipe name 
		PIPE_ACCESS_DUPLEX,       // read/write access 
		PIPE_TYPE_BYTE |       // message type pipe 
		PIPE_READMODE_BYTE |   // message-read mode 
		PIPE_WAIT,                // blocking mode 
		PIPE_UNLIMITED_INSTANCES, // max. instances  
		BUFSIZE,                  // output buffer size 
		BUFSIZE,                  // input buffer size 
		0,                        // client time-out 
		NULL);                    // default security attribute 

	if (hPipe == INVALID_HANDLE_VALUE)
	{
		_tprintf(TEXT("CreateNamedPipe failed, GLE=%d.\n"), GetLastError());
		return -1;
	}

	// Wait for the client to connect; if it succeeds, 
	// the function returns a nonzero value. If the function
	// returns zero, GetLastError returns ERROR_PIPE_CONNECTED. 

	BOOL fConnected = ConnectNamedPipe(hPipe, NULL) ?
		TRUE : (GetLastError() == ERROR_PIPE_CONNECTED);

	if (fConnected)
	{
		printf("Client connected...\n");
	}
}

void run() {
	CreatePipe();

    ST::CaptureSessionSettings settings;
    settings.source = ST::CaptureSessionSourceId::StructureCore;
    settings.structureCore.depthEnabled = true;
    settings.structureCore.visibleEnabled = false;
    settings.structureCore.infraredEnabled = true;
    settings.structureCore.accelerometerEnabled = false;
    settings.structureCore.gyroscopeEnabled = false;
    settings.structureCore.depthResolution = ST::StructureCoreDepthResolution::VGA;
	settings.structureCore.depthRangeMode = ST::StructureCoreDepthRangeMode::Short;
	settings.structureCore.dynamicCalibrationMode = ST::StructureCoreDynamicCalibrationMode::Off;
	settings.structureCore.initialInfraredGain = 3;
	settings.structureCore.initialInfraredExposure = 0.03;
	settings.structureCore.disableInfraredIntensityBalance = true;
    settings.structureCore.imuUpdateRate = ST::StructureCoreIMUUpdateRate::AccelAndGyro_200Hz;
	settings.structureCore.infraredMode = ST::StructureCoreInfraredMode::BothCameras;
	settings.structureCore.infraredAutoExposureEnabled = true;
	settings.applyExpensiveCorrection = true;

    SessionDelegate delegate;
    ST::CaptureSession session;
    session.setDelegate(&delegate);
    if (!session.startMonitoring(settings)) {
        printf("Failed to initialize capture session!\n");
        exit(1);
    }

    /* Loop forever. The SessionDelegate receives samples on a background thread
       while streaming. */
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

int main(void) {
    run();
    return 0;
}
