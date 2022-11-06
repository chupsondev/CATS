import dearpygui.dearpygui as dpg
from tests import TestSet

# settings
fileDialogWidth = 700
fileDialogHeight = 400
windowWidth = 1200
windowHeight = 600
windowDimensions = (windowWidth, windowHeight)

filePath = None
fileName = None
fileNameNoExtension = None


def chooseFile(sender, data):
    dpg.configure_item("fileDialog", show=True)


def fileChosen(sender, data):
    global filePath, fileName, fileNameNoExtension
    filePath = data['file_path_name']
    fileName = data['file_name']
    fileNameNoExtension = fileName.split(".")[0]
    dpg.set_value("filePath", "File path: " + filePath)
    dpg.configure_item("editTestsButton", show=True)


def test():
    t = TestSet(filePath, fileName, fileNameNoExtension)
    print(t.getTests())


def editTests():
    testForFile = TestSet(filePath, fileName, fileNameNoExtension).getTests()
    if testForFile is None:
        return
    # with dpg.window(label="Edit tests", width=windowWidth-20, height=windowHeight-20, no_resize=True, no_move=True):


def main():
    dpg.create_context()  # create dearpygui context

    # font settings
    dpg.set_global_font_scale(0.75)
    with dpg.font_registry():
        font = dpg.add_font("OpenSans-Regular.ttf", 15 * 2, tag="ttf-font")
        biggerFont = dpg.add_font("OpenSans-Regular.ttf", 20 * 2, tag="biggerFont")
    dpg.bind_font("ttf-font")

    # primary window
    with dpg.window(tag="primary"):
        header = dpg.add_text("Please choose the file you want tested.")
        dpg.add_button(label="Choose file", callback=chooseFile)
        with dpg.file_dialog(directory_selector=False, show=False, callback=fileChosen, tag="fileDialog", min_size=(
                fileDialogWidth, fileDialogHeight)):
            dpg.add_file_extension(".exe", color=(255, 0, 0, 255), tag="exeExtension", custom_text="[Executable file] ")
        filePathText = dpg.add_text("File path: ", tag="filePath")
        dpg.add_spacer(height=30)
        dpg.add_button(label="Edit test for this file", callback=editTests, show=False, tag="editTestsButton")
        dpg.add_spacer(height=15)
        dpg.add_button(label="Run test", tag="run", callback=test, width=200)
        dpg.bind_item_font(header, "biggerFont")

    dpg.create_viewport(title="Algorithm Checker", width=windowWidth, height=windowHeight)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_primary_window("primary", True)

    # main loop
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()


main()
