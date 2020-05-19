from PIL import Image, ImageDraw, ImageFont
import numpy as np
import dropbox
human_unit = 23

#draw.text((10, 10), fill=(0, 0, 255), font=font)
MF = 1
#dbx = dropbox.Dropbox('JUSy-o0vW0gAAAAAAAAAnWt-oe9m54xJMIiK6xoR7aPuUDKdJdCc0_hU1POafwNA')
#dbx.users_get_current_account()
#dbx.files_download_to_file('kekka.csv','/backup/kekka.csv')
raw_data = open("kekka.csv", 'r')
data = np.loadtxt(raw_data, delimiter=",")
dd_mae = data[np.where(data[:,MF] == human_unit)]
raw_data.close()
dd_usiro =[]	
#dd = np.append(dd, np.array([[1],[2]]), axis=1)
for num,i in enumerate(dd_mae):
    #print(i)
    if MF == 0:#MEN
        dd_usiro.append(np.append( dd_mae[num], i[7]/i[5] )) 
        #pass
    else :#WOMEN
        dd_usiro.append(np.append( dd_mae[num], i[6]/i[4] )) 
print(dd_usiro)
dd_mae = np.array(dd_usiro)
dd_usiro =[]	
#dd = np.append(dd, np.array([[1],[2]]), axis=1)
for num,i in enumerate(dd_mae):
    #print(i)
    if MF == 0:#MEN
        dd_usiro.append(np.append( dd_mae[num], i[2]+i[3]+i[7]+i[5] )) 
        #pass
    else :#WOMEN 
        dd_usiro.append(np.append( dd_mae[num], i[2]+i[3]+i[4]+i[6] ))
print(dd_usiro)
dd = np.array(dd_usiro)
dd_kekka = []
dd_sort = dd[np.argsort(dd[:, 2])[::-1]]#共分散
dd_kekka.append(dd_sort[0])
dd_sort = dd[np.argsort(dd[:, 3])[::-1]]#時間荷重
dd_kekka.append(dd_sort[0])
if MF == 0:
    dd_sort = dd[np.argsort(dd[:, 5])[::-1]]#WOMEN笑顔
    dd_kekka.append(dd_sort[0])
else:
    dd_sort = dd[np.argsort(dd[:, 4])[::-1]]#MEN笑顔
    dd_kekka.append(dd_sort[0])

dd_sort = dd[np.argsort(dd[:, 8])[::-1]]#YOU上むいている
dd_kekka.append(dd_sort[0])
dd_sort = dd[np.argsort(dd[:, 9])[::-1]]#最終評定
dd_kekka.append(dd_sort[0])
dd_so = np.array(dd_kekka)
#print(dd_so[:,1])

#画像の読み込み
img = Image.open("250293.jpg")
#drawインスタンスを生成
draw = ImageDraw.Draw(img)
#フォントの設定(フォントファイルのパスと文字の大きさ)
font = ImageFont.truetype("C:\Windows\Fonts\meiryob.ttc", 27)
#文字を書く
wi = 380
di = 435
print(dd_so)
if MF == 0:
    draw.text((184, 285), str(int(human_unit)), fill=(255, 255, 255), font=font)
    draw.text((wi, di), str(int(dd_so[0,1])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+90), str(int(dd_so[3,1])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+175), str(int(dd_so[1,1])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+260), str(int(dd_so[2,1])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+350), str(int(dd_so[4,1])), fill=(255, 255, 255), font=font)
else:
    draw.text((184, 285), str(int(human_unit)), fill=(255, 255, 255), font=font)
    draw.text((wi, di), str(int(dd_so[0,0])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+90), str(int(dd_so[3,0])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+175), str(int(dd_so[1,0])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+260), str(int(dd_so[2,0])), fill=(255, 255, 255), font=font)
    draw.text((wi, di+350), str(int(dd_so[4,0])), fill=(255, 255, 255), font=font)

img.save("conv.jpg")
img_resize= img.resize((120,240))
img_resize.save("conv_resize.jpg")