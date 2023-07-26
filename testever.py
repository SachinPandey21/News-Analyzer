from flask import Flask, request
import string
from collections import Counter
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as soup
from datetime import date
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)


@app.route('/')
def index():
    return '''

       <html>
            <head>
            <style>
                @import url(https://fonts.googleapis.com/css?family=Lato);
                html, body {
                padding: 0;
                margin: 0;
                height: 100%;
                }

                html {
                font: 1em/1.5 "Lato", sans-serif;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                text-rendering: optimizelegibility;
                }

                body {
                  font-size: 1.3em;
                }

                header {
                  height: 100%;
                  position: relative;
                  overflow: hidden;
                  background: url(https://unsplash.imgix.net/45/ZLSw0SXxThSrkXRIiCdT_DSC_0345.jpg?q=75&w=1080&h=1080&fit=max&fm=jpg&auto=format&s=857f07b76abac23a7fb7161cc7b12a46) center no-repeat;
                  /* Image Credit: Unsplash.me */
                  background-size: cover;
                }
                header .content {
                  position: absolute;
                  top: 0;
                  left: 0;
                  right: 0;
                  bottom: 0;
                  z-index: 1;
                }

                header h1, header h2 {
                  margin: 0;
                }
                header h2 {
                  text-transform: uppercase;
                  margin-top: -.5em;
                }

                header hgroup {
                  -webkit-transform: translate(-50%, -50%);
                  -moz-transform: translate(-50%, -50%);
                  -ms-transform: translate(-50%, -50%);
                  -o-transform: translate(-50%, -50%);
                  transform: translate(-50%, -50%);
                  display: inline-block;
                  text-align: center;
                  position: absolute;
                  top: 50%;
                  left: 50%;
                  color: #fff;
                  border: 5px solid #fff;
                  padding: .5em 3em;
                  background-color: rgba(0, 0, 0, 0.2);
                  z-index: 2;
                }

                header .overlay {
                  position: absolute;
                  top: 0;
                  right: 0;
                  left: 0;
                  bottom: 0;
                  background:#333 center no-repeat;
                  background-size: cover;
                  z-index: 0;
                  opacity: 0;  -webkit-filter: blur(4px);
                }
                img{
                  margin-right:20px
                }
                .site {
                  padding: 20em 0;
                  text-align: center;
                  background-color: #efefef;
                  font-size: .8em;
                  color: #444;
                  position:relative
                }
                .site a {
                  color: #666;
                  text-decoration: none;
                }
                .site a:hover {
                  color: #222;
                }

                .site nav{
                  position:absolute;
                  top:0;
                  left:0;
                  background:#222;
                  width:100%
                }
                .site nav a{
                  padding:10px 30px;
                  font-size:1.3em;
                  display:inline-block
                }
                .site nav a:hover{
                  background:#333;
                  color:#fff
                }

                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;900&display=swap');

                input {
                  caret-color: red;
                }
                
                
                .container {
                  position: relative;
                  width: 350px;
                  height: 500px;
                  border-radius: 20px;
                  padding: 40px;
                  box-sizing: border-box;
                  background: #ecf0f3;
                  box-shadow: 14px 14px 20px #cbced1, -14px -14px 20px white;
                  
                  
                  
                  
                  background: #efefef;
                  display: flex;
                  align-items: center;
                  text-align: center;
                  justify-content: center;
                  place-items: center;
                  overflow: hidden;
                  font-family: poppins; 
                  
                }
                
                .inputs {
                  text-align: left;
                  margin-top: 30px;
                }
                
                label, input {
                  display: block;
                  width: 100%;
                  padding: 0;
                  border: none;
                  outline: none;
                  box-sizing: border-box;
                }
                
                label {
                  margin-bottom: 4px;
                }
                
                label:nth-of-type(2) {
                  margin-top: 12px;
                }
                
                input {
                  background: #ecf0f3;
                  padding: 10px;
                  padding-left: 20px;
                  height: 50px;
                  font-size: 14px;
                  border-radius: 50px;
                  box-shadow: inset 6px 6px 6px #cbced1, inset -6px -6px 6px white;
                }
                
                
                
                
                
                
                
                
                
                @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700;800;900&display=swap");

                .footer {
                  position: relative;
                  width: 100%;
                  background: #3586ff;
                  min-height: 100px;
                  padding: 20px 50px;
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  flex-direction: column;
                }
                
                .social-icon,
                .menu {
                  position: relative;
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  margin: 10px 0;
                  flex-wrap: wrap;
                }
                
                .social-icon__item,
                .menu__item {
                  list-style: none;
                }
                
                .social-icon__link {
                  font-size: 2rem;
                  color: #fff;
                  margin: 0 10px;
                  display: inline-block;
                  transition: 0.5s;
                }
                .social-icon__link:hover {
                  transform: translateY(-10px);
                }
                
                .menu__link {
                  font-size: 1.2rem;
                  color: #fff;
                  margin: 0 10px;
                  display: inline-block;
                  transition: 0.5s;
                  text-decoration: none;
                  opacity: 0.75;
                  font-weight: 300;
                }
                
                .menu__link:hover {
                  opacity: 1;
                }
                
                .footer p {
                  color: #fff;
                  margin: 15px 0 10px 0;
                  font-size: 1rem;
                  font-weight: 300;
                }
                
                .wave {
                  position: absolute;
                  top: -100px;
                  left: 0;
                  width: 100%;
                  height: 100px;
                  background: url("https://i.ibb.co/wQZVxxk/wave.png");
                  background-size: 1000px 100px;
                }
                
                .wave#wave1 {
                  z-index: 1000;
                  opacity: 1;
                  bottom: 0;
                  animation: animateWaves 4s linear infinite;
                }
                
                .wave#wave2 {
                  z-index: 999;
                  opacity: 0.5;
                  bottom: 10px;
                  animation: animate 4s linear infinite !important;
                }
                
                .wave#wave3 {
                  z-index: 1000;
                  opacity: 0.2;
                  bottom: 15px;
                  animation: animateWaves 3s linear infinite;
                }
                
                .wave#wave4 {
                  z-index: 999;
                  opacity: 0.7;
                  bottom: 20px;
                  animation: animate 3s linear infinite;
                }
                
                @keyframes animateWaves {
                  0% {
                    background-position-x: 1000px;
                  }
                  100% {
                    background-positon-x: 0px;
                  }
                }
                
                @keyframes animate {
                  0% {
                    background-position-x: -1000px;
                  }
                  100% {
                    background-positon-x: 0px;
                  }
                }
                

            </style>                     
            </head>


            <body>
            <header>
                <div class="content">
                    <hgroup>
                        <h1>THE NEWS OF OUR TIME</h1>
                        <i>"Stay Informed. Empower Your World."</i>
                    </hgroup>
                </div>
                <div class="overlay"></div>
            </header>

            <section class="site">
                <nav>
                    <a href="https://www.news18.com/livetv/" target="_blank">NEWS18</a>
                    <a href="https://edition.cnn.com/" target="_blank">CNN</a>
                    <a href="https://indianexpress.com/" target="_blank">TheIndianEXPRESS</a>
                </nav>
                
                
                
                <div class="hwrap"><div class="hmove">
                  <div class="hitem"><p style="color:red" ><strong><font size="+2">Breaking News Analyzer</font></strong></p></div>
                </div>
                
                
                
                
                
                <blockquote>
                    <img src="https://media-public.canva.com/cyI2w/MADmjMcyI2w/2/s2-1.svg"  >
                </blockquote>

                
                         
                <center>         
                <div class="container">
                  <form method = 'post'> 
                      <div class="inputs">
                            <label>Enter link</label>
                            <input type="text" id="link" name="link" ><br>
                            <label>Enter one of the following:-<br>
                                        -> div <br>
                                        -> h5  <br>
                                        -> h4  <br>
                                        -> h3  <br>
                                        -> h2  <br>
                                        -> p  
                                    <br> </label>
                            <input type="text" id="custom" name="custom" ><br><br>
                            <input type="submit" value="submit">
                      </div>
                  </form>
                </div>  
                </center>         
                
               
               </section> 
               
                <footer class="footer">
                    <div class="waves">
                      <div class="wave" id="wave1"></div>
                      <div class="wave" id="wave2"></div>
                      <div class="wave" id="wave3"></div>
                      <div class="wave" id="wave4"></div>
                    </div>
                    <ul class="social-icon">
                      <li class="social-icon__item"><a class="social-icon__link" href="#">
                          <ion-icon name="logo-facebook"></ion-icon>
                        </a></li>
                      <li class="social-icon__item"><a class="social-icon__link" href="#">
                          <ion-icon name="logo-twitter"></ion-icon>
                        </a></li>
                      <li class="social-icon__item"><a class="social-icon__link" href="#">
                          <ion-icon name="logo-linkedin"></ion-icon>
                        </a></li>
                      <li class="social-icon__item"><a class="social-icon__link" href="#">
                          <ion-icon name="logo-instagram"></ion-icon>
                        </a></li>
                    </ul>
                    <ul class="menu">
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/trending/" target="_blank" >Trending News</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/sports/" target="_blank" >Sports News</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/entertainment/" target="_blank">Entertainment</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/technology/mobile-tabs/" target="_blank" >Technology</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/health-wellness/" target="_blank">Health News</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/Jobs/" target="_blank">Jobs</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/business/" target="_blank">Business News</a></li>
                      
                
                    </ul>
                    <p>&copy;2023 Sachin Pandey | All Rights Reserved</p>
                    <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
                    <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
               </footer>
            
            
            </body>

       </html>

    '''


@app.route('/', methods=['POST'])
def news_scrap_and_sentiment():
    link = request.form['link']
    scrap_from = request.form['custom']

    today = date.today()
    d = today.strftime("%d-%m-%y")  # today's date

    cnn_url = link.format(d)
    html = requests.get(cnn_url)

    def newsReport():
        new_news = []
        bsobj = soup(html.content, 'lxml')
        for link in bsobj.findAll(scrap_from):
            new_news.append(link.text)
        return new_news

    text = ""
    text_news = newsReport()
    length = len(text_news)

    for i in range(0, length):
        text = text_news[i] + " " + text

    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = word_tokenize(cleaned_text, "english")

    final_words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)

    emotion_list = []
    with open('emotions', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')

            if word in final_words:
                emotion_list.append(emotion)

    w = Counter(emotion_list)  # print counter

    def sentiment_analyse(sentiment_text):
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)  # score printing
        if score['neg'] > score['pos']:
            return "Negative Sentiment"
            # print("Negative Sentiment")                                                                               #negative sentiment
        elif score['neg'] < score['pos']:
            return "Positive Sentiment"
            # print("Positive Sentiment")                                                                               #positive sentiment
        else:
            return "Neutral Sentiment"
            # print("Neutral Sentiment")                                                                                #neutral sentiment

    def for_score(sentiment_text):
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        return score

    sentiment = sentiment_analyse(cleaned_text)
    score = for_score(cleaned_text)

    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()  # auto tilt the x-axis labels when they are mixing with each other.
    # plt.savefig('graph.png')
    plt.show()

    return '''
    <body style="margin:0;padding:0;font-family: sans-serif;background: linear-gradient(#141e30, #243b55);">
        <div class="container" style="border-radius: 5px;background-color: #f2f2f2;padding: 20px;">
              <form style=" padding: 16px;width: 16px*20;margin: 0 auto;">
                    <h3><center><strong style="color:red;">ANALYZED SENTIMENT</strong><center></h3><br>
                    <label for="fname" style=" font-size: $ruler;" ><strong>Today's Date: </strong> {}</label><br>
                    <label for="lname" style="font-size: $ruler;" ><strong>Counter: </strong>{}</label><br>
                    <label for="lname" style="font-size: $ruler;" ><strong>Score: </strong>{}</label><br>
                    <label for="sentiment" style="font-size: $ruler;" ><strong>Sentiment after reading: </strong><strong style="color:red;">{}</strong></label><br><br>
                    <label for="lname" style="font-size: $ruler;" ><strong>Text: </strong>{}</label><br>
              </form>
        </div>
    </body>
    '''.format(d, w,score, sentiment, text)





if __name__ == '__main__':
    app.run()
