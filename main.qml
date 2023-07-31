import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
Window {
    visible: true
    width: 750
    height: 680
    title: "Example Window"
    Material.theme: Material.Light
    Material.accent: Material.Blue
    MenuBar {
        id: menuBar
        Menu {
            title: "File"
            MenuItem {
                text: "Logout"
                onTriggered: my_class.cppSlot()
            }
            MenuItem {
                text: "Connect"
                onTriggered: console.log("Connect clicked")
            }
            MenuItem {
                id: exitAction
                text: "Exit"
                onTriggered: close()
            }
        }
        Menu {
            title: "Settings"
            MenuItem {
                text: "Change Font"
                onTriggered: console.log("Copy clicked")
            }
            MenuItem {
                text: "Modify Settings"
                onTriggered: my_class.cppSlot()
            }
        }
    }

    ScrollView {
        id: scrollView
        anchors.top: menuBar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 10
        clip: true
        TextArea {
            id: myTextArea
            width: scrollView.width
            height: scrollView.height
            font.pixelSize: 20
            wrapMode: Text.WrapAnywhere
        }
    }

    Button {
        id: button1
        text: "Program"
        anchors {
            bottom: button2.top
            right: parent.right
            margins: 25
        }
        height: 65;
        width: 140;
        font.pixelSize: 20
        onClicked: my_class.cppSlot()
    }

    Button {
        id: button2
        text: "Test"
        anchors {
            bottom: parent.bottom
            right: parent.right
            margins: 25
        }
        height: 65;
        width: 140;
        font.pixelSize: 20
        onClicked: my_class.cppSlot()
        onDoubleClicked: console.log("Button 2 double clicked")
    }


}

