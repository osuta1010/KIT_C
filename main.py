from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)
import os
import dropbox
from dropbox.files import WriteMode
import datetime
import numpy as np
import math
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def writing(words):
    dbx = dropbox.Dropbox('JUSy-o0vW0gAAAAAAAAAnWt-oe9m54xJMIiK6xoR7aPuUDKdJdCc0_hU1POafwNA')
    dbx.users_get_current_account()
    dbx.files_download_to_file('/tmp/log.txt','/backup/backup.txt')
    now = datetime.datetime.now()
    with open("/tmp/log.txt","a") as f:
        f.write(words+'\t{0:%Y%m%d%H%M%S}\n'.format(now))
    with open('/tmp/log.txt', 'rb') as f:
        dbx.files_upload(f.read(),'/backup/backup.txt',mode=WriteMode('overwrite'))

def index(human_unit):
    if human_unit >= 1 * 10**int(math.log10(human_unit)) and human_unit < 2 * 10**int(math.log10(human_unit)) :
        MF = 0
    elif human_unit >= 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):
        MF = 1
    
    dbx = dropbox.Dropbox('JUSy-o0vW0gAAAAAAAAAnWt-oe9m54xJMIiK6xoR7aPuUDKdJdCc0_hU1POafwNA')
    dbx.users_get_current_account()
    dbx.files_download_to_file('/tmp/kekka.csv','/backup/kekka.csv')
    raw_data = open("/tmp/kekka.csv", 'r')
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
            dd_usiro.append(np.append( dd_mae[num], i[7]/i[5] )) 
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
    dd_so = np.array(dd_kekka)
    print(dd_so[:,1])
    dbx.files_download_to_file('/tmp/249644.jpg','/backup/249644.jpg')
    #画像の読み込み
    img = Image.open("/tmp/249644.jpg")
    #drawインスタンスを生成
    draw = ImageDraw.Draw(img)
    #フォントの設定(フォントファイルのパスと文字の大きさ)
    font = ImageFont.truetype("/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'", 27)
    #文字を書く
    draw.text((460, 510), str(int(dd_so[0,1])), fill=(255, 255, 255), font=font)
    draw.text((460, 600), str(int(dd_so[3,1])), fill=(255, 255, 255), font=font)
    draw.text((460, 685), str(int(dd_so[1,1])), fill=(255, 255, 255), font=font)
    draw.text((460, 770), str(int(dd_so[2,1])), fill=(255, 255, 255), font=font)
    #draw.text((460, 858), str(dd_so[4,1]), fill=(255, 255, 255), font=font)
    img.save("/tmp/conv.jpg")
    img_resize= img.resize((240,240))
    img_resize.save("/tmp/conv_resize.jpg")
    

def poow(num):
    return num * num

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    human_unit = int(event.message.text) 
    
    #dd = index(human_unit)
    words=""
    if human_unit == 11:
    #if human_unit < 2 * 10**int(math.log10(human_unit)) :#man
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
            original_content_url="https://lh3.googleusercontent.com/3zpGSZQ_NW5GYJs1uYFFyu5xjdUm24BOMT_lR2-jtbOeKncPGB9VNANrV9pP2z5Hh_7b0JQWBYv6-hZ2BeZ6PZNRsPST-Et5nHAikllRhnJgmSPENmY79qb9atCBBA1ADJWiD8qWwELUa13Z26q1ySz5ARrX2cvMa0VivRjfrgbDu7_kOT8ZPuXDv29UZZDcIXoMwFHhiwFz5UsCXmwZmzgmCsXN7BAztLi7knFy_KVJcQgQUQg4XjUWfsB08iffSdGx9C9xO8jiUCx9NMfOiXhzywxWdGFeL6XuMX5FjkyXO6nusDH57zivepiRKXa6RyU7Och_V3zMAK3YaCdj36T46EeikgFlC87xh1PvBxHv3KwOSFTgjM-pEpQjHv5Wh1Eex54by10FYPuA86wD6SWbOBnV7KHZX5PsFwa5oW5akYA-bgbMhyqMc7dWWrYDiUX9123DXwBE9pakbvFrFWyHZle5XdqSkUIUoaR7k59UAzURyUIwGuyTykzr7o5Y-xx4uoFeLE4f6QPePUHW07mkkYspoQJ4_fXe_JeNj6TYQeZBGVPdIzbWqIgYgXb9NuEIckjDJp9iMtRcN1fm8CoTqDuiKazg-VMH1a1AQIQz4SwPGtJUUaaUQxWSZiI0r-YlIaAl_XP7OHhMAL7N0-c7=w440-h879-no",
            preview_image_url="https://lh3.googleusercontent.com/5BKhLaNGhI5BeSHKmHkQnIC0Bz022D4Xk4wgjMeKdJfAqGJCgoTg4YdTykXC-iAh9FPAU_sq8-tddhfM23pIpRzIFr3yHZ9zWIKihd4Y2uli38hGg7Xvja7AV7BEtJ5RelPxsoGDsRl4UxZDGuh4ES6wPEH0iQKC1Ju_qbWRYf-v-4GejYm8aGNGlixbg1UR2Qe62JnbAGOGVQ_YSb1shVew1FOr_xAUxknOKRfOug5BBvPCTav3Usdb7WHASI7hJnxAzoBg3LrveK1SaJYfNHMpCkocknKq9gHMvL1lW-_2lIkMFNFUGsYqUKRg0LslH3IPIWeKo-CzM61GPBVk8DxAeRZeieGoPnP9WOSlkAXp4SiqkMpr6DOTlAtOWyjni_TA1J7Sxc_plYcBsjwwyT8sy7KD-84y9rrkMDcv4qfbgKNlgtDXuZUwQo9lMdpX_cj8CQuBZvXIXgKd1f_fzxoD-AL6R4SWs-0kp2S6OYfRE_wyPxLsdSD4fRCPr53ddtvqeDmkT9aotFh3yTO6hb4Le6gX4SF6ro68m0t0iLUqRLWY1q5O_6Hw9IPhow3OSsaANtxTuSs4vHVlr_VjEmrugzY6lT1k38hgjVEpb4CvE-SwHEwwKe5Jpoh0-YzKhjna1tPmX-Ay1lzW1ZNfolq6=w120-h240-no"
            ))
        writing(event.message.text)
    elif human_unit == 12:
    #elif human_unit >= 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):#woman
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
            original_content_url="https://lh3.googleusercontent.com/JMqafXtBRyiQqg7fGd19poIdyzr2OBUIsclm8zPs7idG-IY0qBNgBLvA0jW7O6Bqwaa-Rnlnf1XemzWYij9E4pAdWME1MABLN4UuwCXcOCWBxrbCl3JDWiP4W1AGXrrr08yCyqp8IPAya6p3kpvSMcqR_Dti-e_UaXJ2blYJhX6jYC_qGu69MyPAqvo8yEkrelPgfDRSWSL72vnptutrq7h3sL_hCnmuywijuRhqJd6D03j5pkWm2bUIgyk3ZheR99UvoGnTzYwsqORPMqZjoJg3eVUzFPTjtR30wcn_pOYWMPPFNLK3jrl3zvnMcp1YtvqlY8RdBX65V8VeRvv7dr67X1SzyMD7dYlFb1nw5jopUiTqO1eMBVV3-9rOn2o9bMsCpPnZT2jcD9q3aHKJvM4ELjf2oexKvji6iIuPIs1D3XWHQgxrMJKKyEfTV40ARJvF1_XoLJgFG_yecD8fUBO2uE1gx-NlTEbSKMP6zALLTa698SpRicLGR4q8MDkdh-YWPlPpKuTzeNcHeVWvhX-SpfBz9qOILr6i4Iufu3sm6XHhsE_Etl9m1VBXuytgILnSHObbmhyJQSPNHS6tnMcnS4He_6bzx1lWBL3FeYXrVtcf0Q6s3O0EgMtI4H4TNmcH2VUa_8QESSSJWdPdgfsJ=w440-h879-no",
            preview_image_url="https://lh3.googleusercontent.com/2EHa0JvjaTsNMmS5-D3GLjMVvWmPyTXAsYwY2eeKcHofAXtZwPR-mXeXx0bVRW0jDY_GFKJ1xcBeiEBlhCgA0AAODox2j72qTq4aSNqQqhxOGuuOR39nEOX0P-1ZCk2Q5j1pq7OuT7Y6Q9X7pzsvsmFbKs7Qk4w3yLpLvd_4RXxMmgMSe9HdmvJLmWSBR_J3Dte_DjU9GgePrcGJIKhOO5f2GpYp_cePIve8G1YZoFwUe-HCYIS9rxNvT9g2-qWd_1qaUjdteRqfIYbWqeSbmGVC4kTVyiHG7zzuX7S3H8sRNjZ8ZYmHKdNtcUS0fpn4ttfUm_z7I40TcSSJYJPbfm7yp1Irp0ftUbLhdWReDF8Ea8raPWUbaVBErUcinPTpBjT-XPYeh1isyYUzJG3bg3rriYJaOQJc8_1xGZDfC2ygUzazaU2MiLuM7-8ScW1Y11Yrf6ZpvFimcAqOc4GGRbRmtZbTR2GKDFTUumNGTnpJsnHrCWkUoKmVqY87QNhtdWJCxZ8lUe0Yol4aJ80gHbGf8cHNLinIZ6b066JCHWTiI92wgTnIImlLQ9HfdaqOX7KYCNsfDShboiRQy1MDEeuPqOKwtZI3x4kYJDYcB5Vc1FgkQDXLXMeHSuBLJlczgQ0d9FVXWT-q6ypCQubEgTqs=w120-h240-no"
            ))
        writing(event.message.text)
    if human_unit == 13:
    #if human_unit < 2 * 10**int(math.log10(human_unit)) :#man
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
            original_content_url="https://lh3.googleusercontent.com/Y6rSUN0wzevGfG54amWU9Q8d6M-3TlEk9sbJAFfrqZGHWRo0D9GjclSwog3A8YeoPKhiFrhSAdY-_77CrLL8EPPsxL-kJQJw1w__KYOJzJ7kqZaZoVUUBsyrLSZwfA8XC8WXSociETNNdcY6cfsRk4rApo_oybJ2BdtlXtA5_5uoG1YXTwyuTA3XFOtSvYj8wURhsVjgZtaE-ODKGGBlyBDIVBOmBEMSvlSXgKQmMRbTCASjjrHlRvZK432QB1zMm-hVh7ZDicMg7NvUmYhb827QFP-3TLZxRaIIJH9lhuU9BLeZsZbZ9yHyjuVZvd5TWoqOcJ0JyZ4f-nd2CMfYPq7lnW9Yi76rTa52TojkwIlYSfb2ia7ubXyt23EwbApox7V6Rb1G88qGsP1pjaJgvqPRriIPohLsojwKHSjvleq8Jp23bda-lQVZlT8JN75HKLHZ5Y3ca3v-pvvnGGJUWIaa0W4gFrmQEHkjTvbP1_WKGs-z36PQNVwBoVpPkDcIfYXHU1NotX_1wzuYw35nBYPlJKP1anRVZ-3g872qGLUCLcbwAwbn97QfWjpKKStyZSPSk8fm2gNWFnFxEKRthj6HkFyG53sHTroZAIn05ioev0bvG6B2lBT8LqIps-1ZYpfgLVKZQKa7jEIXpIV9XhmR=w440-h879-no",
            preview_image_url="https://lh3.googleusercontent.com/ctQp9_9H69k1zy9hS2PfexWgdOprU5W1Gd4xP8meaMl_9VMdLdZDQLW0KvG6Tf542CnzIFTQRYUR_cbBxjGCiFR6RU3ou74WOyBzz8VK1k7O6S7CYbEQjSrubp5nzCzpXOv337aFliTh5_qZeZl65pbecDu0oSKfkYegimnR2vIwuco1a1BnOC8v0W-s4PuXj_jXqJEC5opxunXWX_mC_vHPCKoRFC1z4uP6_WRHng8w_6dEPpC9HS6w44dWNyznSc-UsBa8WaZrHRQjnNZHR09NMDItuI62CJqVHTdSzQoRigEKhAneHIY3uPrMHZiePPYU-Dwsz-_Uz5v5362vPPPdA2Gn6aPEERbeAia817ru08u1xXv9ZrZMHIE0u7-yBgC3GH5FrnViyBCL7NB7E5TvR08q4XOoIIsaMVIvW7yKxTYasss-XTLygaeqtiCDAJsOh-FxJKZzc2kze2uoPqKYfcPfiuW8Gft2LsWE8xBjQWblBnh2y2anbrgNJkET8AmKfwRO6RN-gKC698W3q6i2oHkXIpCFA9U45tfkrHSRKbL38tuAded7Oj9fZxa-KKT2X-AhJ9vQOaAyssxooBhAfqJdJ6ScoPdm9bO-YqX2bxsT6JbAlm3TY2vdw-knuJnMtNxvLa08-qPpGXdNu86f=w120-h240-no"
            ))
        writing(event.message.text)
    elif human_unit == 21:
    #elif human_unit >= 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):#woman
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
            original_content_url="https://lh3.googleusercontent.com/fvrR9A03dv_TI4s18hqCXKjG_UKSq0PcVd0HKouVHcJ5ul32plPDA-bilP5N5V8D_57M2SudZLii8VhFOMaQo-SmGpQsu2u9uWBbBgpjareqHj33XzbdvR5ZdKgH2G9CadNOAfmHoSXTY7akvdWBHStkPj67ypIV3R9JOQ9PyXr-XVVKNj6BRfwPTFxhoi0PMRah6gDFcqkGRagVjGPG4wtdlOFhWUpy5QqDPVv3kFwBR6-LtdV0bdnJ0rPzZhISUwQL7kZUrYUHkh5yV0Vf9ITSHImYb-G4HKMc9Gt9t6J1xpFjRfaaUso0tGgnN9ZveRyNVXF7RHYy4x-fJRQQz1wNFF2YMokgiT61P_OJhQ5Om8FaOIuM9CY4RGlvONTELWsGXbznMaNUF5YAYRdMHHZ6i04XIFAKXaFSqZvw8E_F3YjNRDWqnu2yPRZMy94Wm4ApJXFkzbmWyzkGAe7KwcImjcGWQm8iMDzO7gshUXmmnKjyIXFXiqKHiuiO3zMk3HgOUtVIvZdp-ud0EKTeR1-0RPTuEcaxwqWKZCwRTh2eoTksKb9igcXT8rm0GDAaN_RCZQMWmsPtOBd3fy_q_ZpOWYfomXv81xyr9CB0sU7nMkoLv_ef4Zt9m18iRxnzb1gf5_k7iwwwZ4x4tK2C5gUX=w440-h879-no",
            preview_image_url="https://lh3.googleusercontent.com/gaV37KzhNPjHm5HlANqTbMR7aBXQl58OQN-GuxMrMm_ztHfdLGgpIMn5PL9pxUi36B4G_kjXSG3jMuJ_nPIEI--Q_M9lr3KkABM8OeJdMMwPpHm9csLRco_5-uz6-y612WJOSiw51YIJTfr0nKZUITBN4hZAIm8le06gPGaS1_4V2nwJ-QIqTb2HEWsyh8rTFbfpFUJiA2Yzl8iIz2DfPyl_zKm9fcx1p6vdo8pSJtMe34xaf5cD22qTvfImFHafKqfXaX0VRKfqu-Qxm1MiS1oHsyLHhhgdW7zzLbiMtcItf9wGU0NhJDPpH15d_rA2LpWKqsUNlUH3ehg7lEODq3oa6OGLGfUo5Mnna8cGunO8v1jcDxIUEA4B7yTS5c0oBX-L9TCU0DixoKEDH75KInQabMgl2X49WvkOgslEu9sZ_TpGKhCgsycgamv7LzBkD-xKfdRZUH4p3c1h7KeMf8RILZQLW-HuwqJ2DKFSDRJw-Dde35kA4a0p54sIHRII6Irz9T2AErEbQwORvSOwWKGnsBh8e86Z7abZnetPz3vg1fFdkO6O_7IFJDxIEFPhOYATRXReLPeimuHk_w3wczOokUoAoA6LO2q3l-5Nvca16C3eTur5_SFEg7XCN1IitwzDKN3If7aQQrMRviH6KsmW=w120-h240-no"
            ))
        writing(event.message.text)
    if human_unit == 22:
    #if human_unit < 2 * 10**int(math.log10(human_unit)) :#man
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
            original_content_url="https://lh3.googleusercontent.com/zbFwxjMtiBMwRa45b7w7zDpBansaSF8O3Zn4Gy2nqt5TIV6sB1zJgwU67f17WqGXt3VAdhSs3-_HQuTUkoqJBO6hxd5Ohs_EPPTyKHvwZXneHw1MtoCNhLmRnN-lKBApnKlr4ImceTdcF-GHM1zqLUNfBxB2b80_f1x6_NGdP2apfv0hX4-De_RY4d-9KEVfa-cM4FeRW_HsQG9fE7wsXcnJcnpitpVepBdDi0leO4NzBkTxe_dTmb2TtKqG8ZPUpoXfciCtaYmcliG-R2BzxOgRSwn6L3RKaDq_cguljXqL4IOgbnCHdlY3-kI-5FeZy7GkgGnjYba73gUZxN7NHV8AU73LphHNklVD0mHKjBLURcF2ywpow7JthyX1pzAijZ2dlOAAWHlIWD250gmYjj3oYb5vmtChOFGE5rr_eN-Xn21Flz8XvDiwH4GWag-ZzX-IfljkpNoPwTo_Ck4c0CF-_BrRWPij7AunYhfYhEJ7X0OscoryWGZxMqiwfexqq16pq8HnfEb596ZNzhjepJs8BU4MwkX0XwRuQDZJBjzg155dMYIslr-QDBkHrkJYmfWKCpbIAQ7Vs7w6lopSnubDXDhyuBzyK9oMp30mpdrCgQaUA3Eh2pwk-x2pdJlw6Jp7d22K71jwvLxRns1BsIB8=w440-h879-no",
            preview_image_url="https://lh3.googleusercontent.com/4t5t02Lu9MdgFKvWewSnzmmjXDTleckKt_ii70CTXyshbHp-eViOyJhKgeucEpyUMbrwbDx4Vu8nFqI7JYETnshwoCRs1Ee3F5L9tG61PIru7YP7-ig1-agQd7BRaWeEOdsD7r_QqaxuXpIOPVb2KIQRunbf4Cm90-R3ahhfWorRITikZRkvt5Hq9-v7WfMY7iWzcc9yPkTDVfg3AMo4kkOyQaUEitK5Dr-lJLX-vkZ2-ac0rFFbsVFLWser9z490zUIRQXFkQODirEKTAm-kXMjwkAAVBs2rnPlSY_oZZ1oHutKTl4QpybBSdhRr0R1HbBrzxchTnFVjW_lGSQ35TyqXYN8LPILC3EJOLtk91dQWHz4tFlC9pS-ULA69JOmlMsies9DmGXofl2WzT4vLV5Oj2adHl1QxN11E8pHclTBCYuowyx6erWb2gUu5iZk2rmErkevjeXUXSZk_Q_8xqHawexYoGVrA75PdZ_aKVHCUt2mKa8XPXEChFI9jGTQQ8LUsXM9IUD1ICZ8LH5LZmUwirbDJGo7TlwukA6styN-Z9VcE7ZSX2H-6KLCMi86wRqKznKw0QFe46Mxm2mRgCLWGI-Ztw0-MXL16aRITqraZ7kxb3nyPZnBmEsIwTc1E2K3MnWZuaZAnn7ZD8tO7wTv=w120-h240-no"
            ))
        writing(event.message.text)
    elif human_unit == 23:
    #elif human_unit >= 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):#woman
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
            original_content_url="https://lh3.googleusercontent.com/wHZFFuev3ZfEplx160jiUo_tbjJDCWib0mID9MMTJeEoHmg5czI7XVqVoD6mzUZMugMnXSBz6ZOnfeMj4nY9UGZp29l6Zy9ZwTYvrGyHmM6ep3zD8AUUC3cF6anebRluFt1wL801RDe1WZrVFf_IFLp3yxmvwRHQ1Gz_JZl-XunLNNIpnpn7t3z9XIRYVqeOauRze3LPqXUCbSCARvgCyegIWz7eE0dxlw72GVe6Ar6SXdJMP5uAFlMOffhjIG9SznhTyBfj92OcklhTLypd7UJJGd7MAImIeUzlwzTFl8GuH_n_et0_igEJGIK_IbGqzzSe_2wnIwBJY4qqIP-mzI1Gnp90-g0Nqp-SF9mPMpexHOrUr9UVoI-SAPDb1jagXumA9jcasKrH6zekh-h_1FQ682WDlWC0QFx9qx0i8s06V93aMuh6yPsSKOkB6_svgexNk1mQXAqbnwv8RW36shv-NkRPA683SGd2S9A3QOqVyY__XG96iVAdcEjrF4SkZlOolCYjLIWlkLs2_GIRWIaCWHyw1OgVLLVA7dfqhQwiQTeh7W1zz6syplCUeR8YZcRhC94QN2jHcG6g-2BEWDpI45gTp7DcOvIXEkFgntpyFtH_s5FXlohZBachiDnh81fIY07qqgE7cSYKkak9sGGx=w440-h879-no",
            preview_image_url="https://lh3.googleusercontent.com/qHvuNnLqOjpCH0McYBHhY_N7yqP48py6DIwiIYk9ZEU1ILix7eS97dgeyCTUGwjhKjXCLJ1f5eZSA6aNKOP15wZnwkey6ROYVXxX1Z1WdX7_kERMcPMPu0BPYAb_Uo8MMnlBiWCGDOAkVLDdXpADyKAbXTApCSFDpj-3BJcB5MgClYNhS5AY_8DpABLCEu4CLdlnsn5-fHTogBKDAJy-rQ-QDR2_YVpSua1HIrdlKiVH567UdTsqxdNZ55f4EywoczPrNE-8IYMF9zxh9FWRotzVcCmLK7e9MadjVAqETgOMluXzAn6DcVQX5ikX0RFO2mSu9LXX54EIe9CbmM-y9iKTYSmBjgzu4KchcFj7juFaB4svtZJOrBQDIB8GPSpHAZDzOaAHFwcsGbfKofy6_yLfYQ_8G9wai2VsRMu5OBk8yCfSbTVCHGqkJ6CG8nPYeHgtEuHG9ufQuTRVV182si6LvfDB9Lq-prvtRk62kSPATY4Nqh0ukMQFj7MMM5WhYD8S_Xn8dlGlRGInN15QX6ggcoZbbZyScjXU-XzSfD66vu2SC0Wu16fUfsCCLBw8afsSHS8UwFiFgoRhQtSDVh8k2WwDbq9fVr3ljegTeOsXWEeoNadCEcNM17LUL2RuYaGhU_fvsEMXBLojcdSAVph8=w120-h240-no"
            ))
        writing(event.message.text)
    
    


if __name__ == "__main__":
#    app.run()
    
    writing("hello")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)