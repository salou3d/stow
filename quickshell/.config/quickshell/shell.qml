import Quickshell
import Quickshell.Io
import QtQuick

Scope {
    Variants {
        model: Quickshell.screens

        delegate: Component {
            PanelWindow {
                property var modelData
                screen: modelData

                anchors {
                    top: true
                    left: true
                    right: true
                }

                implicitHeight: 24

                Text {
                    id: clock
                    anchors.centerIn: parent
                }
            }
        }
    }

    Process {
        id: dateProc
        command: ["date"]
        running: true

        stdout: StdioCollector {
            onStreamFinished: clock.text = this.text
        }
    }

    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: dateProc.running = true
    }
}
