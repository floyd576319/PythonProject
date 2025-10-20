from gtts import gTTS
import os
import time
#import gTTS,os,time
#固定題目單字
test =['acupuncture','meridian','qi','herbal','decoction'
             ,'pulse diagnosis','tongue diagnosis','moxibustion'
             ,'cupping','energy flow','balance','liver','spleen'
             ,'wind-heat','dampness','cold syndrome','stagnation','nourishing']
#預先生成語音檔
for word in test:
    tts= gTTS(text=word,lang='en') #文字檔轉語音檔
    tts.save(f'{word}.mp3')
#互動測驗開始(開始計分)
print('英文單字聽寫遊戲開始!請根據語音輸入正確拼字。\n')
score =0 #初始化得分
for i,word in enumerate(test): #列出所有單字題目
    print(f'第{i+1}題，請聽...')
    #播放語音檔 Windows
    os.system(f'start {word}.mp3')
    time.sleep(5) #播放等待時間
    #讓學生輸入拼字
    answer =input('請輸入你聽到的單字: ').strip().lower()
    # .strip():去除多餘空白 .lower():統一小寫
    #判斷回答正確與否跟是否加分(判斷式)
    if answer == word:
        print('正確!\n')
        score +=1
    else:
        print('錯誤，正確答案是:{word}\n')
        answer = input('請輸入你聽到的單字: ').strip().lower()
    #顯示學生總得分
    print('測驗結束!')
    print(f'你的得分:{score}/{len(test)}')

