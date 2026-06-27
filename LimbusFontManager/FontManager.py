import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import json

folderdir = None
fontdir = None

root = tk.Tk()

root.title("Limbus Font Changer")
root.geometry("500x340")

deafult_path = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Limbus Company\LimbusCompany_Data",
    r"C:\Program Files\Steam\steamapps\common\Limbus Company\LimbusCompany_Data"
]

def find_game_dir():
    for path in deafult_path:
        if Path(path).exists():
            return path
    return None

def choose_folder():
    global folderdir
    folderdir = filedialog.askdirectory(
        title="LimbusCompany_Data 폴더 선택"
    )
    foldername = Path(folderdir).name
    
    if folderdir:
        if foldername == "LimbusCompany_Data":
            label1.config(fg="green", text=foldername)
        else:
            label1.config(fg="red", text="LimbusCompany_Data 파일 지정 필요")
            folderdir = None

def choose_font():
    global fontdir
    fontdir = filedialog.askopenfilename(
        title="폰트 선택",
        filetypes=[("Font", "*.ttf *.otf")]
    )
    if fontdir:
        name = Path(fontdir).name
        label2.config(fg="green", text=name)

def activate():
    if folderdir is None or fontdir is None:
        label3.config(fg="red", text="위에 두 과정을 선행해주세요.")
        return

    try:
        label3.config(fg="gray", text="작업 시작")
        
        base = Path(folderdir)
        source = base / "Assets" / "Resources_moved" / "Localize" / "kr"
        lang_folder = base / "Lang"
        target = lang_folder / "custom"

        lang_folder.mkdir(exist_ok=True)
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

        for file in target.rglob("*"):
            if file.is_file():
                if file.name.startswith("KR_"):
                    new_name = file.name.replace("KR_", "", 1)
                    new_path = file.with_name(new_name)
                    file.rename(new_path)


        lang_font = target / "Font"
        lang_font.mkdir(exist_ok=True)

        lang_context = lang_font / "Context"
        lang_title = lang_font / "Title"
        lang_context.mkdir(exist_ok=True)
        lang_title.mkdir(exist_ok=True)

        font = Path(fontdir)

        shutil.copy2(font, lang_context / font.name)
        shutil.copy2(font, lang_title / font.name)


    finally:
        label3.config(fg="green", text="작업 완료")
        root.after(2000, root.destroy)


def reactivate():
    if folderdir is None:
        label4.config(fg="red", text="게임 경로를 지정해주세요.")
        return

    try:
        label4.config(fg="gray", text="작업 시작")
        
        base = Path(folderdir)
        source = base / "Assets" / "Resources_moved" / "Localize" / "kr"
        lang_folder = base / "Lang"
        target = lang_folder / "custom"
        fontbackup = base / "FontBackup"
        lang_font = target / "Font"

        if (lang_font).exists():
            if fontbackup.exists():
                shutil.rmtree(fontbackup)

            shutil.copytree(lang_font, fontbackup)


        lang_folder.mkdir(exist_ok=True)
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

        for file in target.rglob("*"):
            if file.is_file():
                if file.name.startswith("KR_"):
                    new_name = file.name.replace("KR_", "", 1)
                    new_path = file.with_name(new_name)
                    file.rename(new_path)

        
        if fontbackup.exists():
            shutil.copytree(fontbackup, lang_font, dirs_exist_ok=True)
            shutil.rmtree(fontbackup)

    finally:
        label4.config(fg="green", text="작업 완료")
        root.after(2000, root.destroy)




frame1 = tk.Frame(root)
frame1.pack(side="top", anchor="w")
button1 = tk.Button(frame1, text="게임 경로 선택", width=25, height=5, cursor="hand2", command=choose_folder)
button1.pack(side="left")
label1 = tk.Label(frame1, text="선택된 경로 없음 [LimbusCompany_Data 파일 선택]")
label1.pack(side="left", padx=10)


frame2 = tk.Frame(root)
frame2.pack(side="top", anchor="w")
button2 = tk.Button(frame2, text="사용 폰트 선택", width=25, height=5, cursor="hand2", command=choose_font)
button2.pack(side="left")
label2 = tk.Label(frame2, text="선택된 폰트 없음")
label2.pack(side="left", padx=10)


frame3 = tk.Frame(root)
frame3.pack(side="top", anchor="w")
button3 = tk.Button(frame3, text="폰트 변경 실행", width=25, height=5, cursor="hand2", command=activate)
button3.pack(side="left")
label3 = tk.Label(frame3, text="위 과정들의 문자가 전부 녹색이 되면 눌러주세요.")
label3.pack(side="left", padx=10)


frame4 = tk.Frame(root)
frame4.pack(side="top", anchor="w")
button4 = tk.Button(frame4, text="폰트 새로고침", width=25, height=5, cursor="hand2", command=reactivate)
button4.pack(side="left")
label4 = tk.Label(frame4, text="현재 폰트로 파일을 새로고침 [경로 지정 필요]")
label4.pack(side="left", padx=10)

folderdir = find_game_dir()

if folderdir:
    label1.config(fg="green", text="LimbusCompany_Data [자동 감지]")
    
root.mainloop()