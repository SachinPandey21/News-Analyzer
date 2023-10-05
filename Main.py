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
                .entries
                {
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
                  z-index: 3;
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

                    body{
                        margin:0;
                        overflow-x:hidden;
                        }

                        .footer{
                        background:#000;
                        padding:30px 0px;
                        font-family: 'Play', sans-serif;
                        text-align:center;
                        }

                        .footer .row{
                        width:100%;
                        margin:1% 0%;
                        padding:0.6% 0%;
                        color:gray;
                        font-size:0.8em;
                        }

                        .footer .row a{
                        text-decoration:none;
                        color:gray;
                        transition:0.5s;
                        }

                        .footer .row a:hover{
                        color:#fff;
                        }

                        .footer .row ul{
                        width:100%;
                        }

                        .footer .row ul li{
                        display:inline-block;
                        margin:0px 30px;
                        }

                        .footer .row a i{
                        font-size:2em;
                        margin:0% 1%;
                        }

                        @media (max-width:720px){
                        .footer{
                        text-align:left;
                        padding:5%;
                        }
                        .footer .row ul li{
                        display:block;
                        margin:10px 0px;
                        text-align:left;
                        }
                        .footer .row a i{
                        margin:0% 3%;
                        }
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








                        .new_footer_top {
                            padding: 120px 0px 270px;
                            position: relative;
                              overflow-x: hidden;
                        }
                        .new_footer_area .footer_bottom {
                            padding-top: 5px;
                            padding-bottom: 50px;
                        }
                        .footer_bottom {
                            font-size: 14px;
                            font-weight: 300;
                            line-height: 20px;
                            color: #7f88a6;
                            padding: 27px 0px;
                        }
                        .new_footer_top .company_widget p {
                            font-size: 16px;
                            font-weight: 300;
                            line-height: 28px;
                            color: #6a7695;
                            margin-bottom: 20px;
                        }
                        .new_footer_top .company_widget .f_subscribe_two .btn_get {
                            border-width: 1px;
                            margin-top: 20px;
                        }
                        .btn_get_two:hover {
                            background: transparent;
                            color: #5e2ced;
                        }
                        .btn_get:hover {
                            color: #fff;
                            background: #6754e2;
                            border-color: #6754e2;
                            -webkit-box-shadow: none;
                            box-shadow: none;
                        }
                        a:hover, a:focus, .btn:hover, .btn:focus, button:hover, button:focus {
                            text-decoration: none;
                            outline: none;
                        }



                        .new_footer_top .f_widget.about-widget .f_list li a:hover {
                            color: #5e2ced;
                        }
                        .new_footer_top .f_widget.about-widget .f_list li {
                            margin-bottom: 11px;
                        }
                        .f_widget.about-widget .f_list li:last-child {
                            margin-bottom: 0px;
                        }
                        .f_widget.about-widget .f_list li {
                            margin-bottom: 15px;
                        }
                        .f_widget.about-widget .f_list {
                            margin-bottom: 0px;
                        }
                        .new_footer_top .f_social_icon a {
                            width: 44px;
                            height: 44px;
                            line-height: 43px;
                            background: transparent;
                            border: 1px solid #e2e2eb;
                            font-size: 24px;
                        }
                        .f_social_icon a {
                            width: 46px;
                            height: 46px;
                            border-radius: 50%;
                            font-size: 14px;
                            line-height: 45px;
                            color: #858da8;
                            display: inline-block;
                            background: #ebeef5;
                            text-align: center;
                            -webkit-transition: all 0.2s linear;
                            -o-transition: all 0.2s linear;
                            transition: all 0.2s linear;
                        }
                        .ti-facebook:before {
                            content: "\e741";
                        }
                        .ti-twitter-alt:before {
                            content: "\e74b";
                        }
                        .ti-vimeo-alt:before {
                            content: "\e74a";
                        }
                        .ti-pinterest:before {
                            content: "\e731";
                        }

                        .btn_get_two {
                            -webkit-box-shadow: none;
                            box-shadow: none;
                            background: #5e2ced;
                            border-color: #5e2ced;
                            color: #fff;
                        }

                        .btn_get_two:hover {
                            background: transparent;
                            color: #5e2ced;
                        }

                        .new_footer_top .f_social_icon a:hover {
                            background: #5e2ced;
                            border-color: #5e2ced;
                          color:white;
                        }
                        .new_footer_top .f_social_icon a + a {
                            margin-left: 4px;
                        }
                        .new_footer_top .f-title {
                            margin-bottom: 30px;
                            color: #263b5e;
                        }
                        .f_600 {
                            font-weight: 600;
                        }
                        .f_size_18 {
                            font-size: 18px;
                        }
                        h1, h2, h3, h4, h5, h6 {
                            color: #4b505e;
                        }
                        .new_footer_top .f_widget.about-widget .f_list li a {
                            color: #6a7695;
                        }


                        .new_footer_top .footer_bg {
                            position: absolute;
                            bottom: 0;
                            background: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEigB8iI5tb8WSVBuVUGc9UjjB8O0708X7Fdic_4O1LT4CmLHoiwhanLXiRhe82yw0R7LgACQ2IhZaTY0hhmGi0gYp_Ynb49CVzfmXtYHUVKgXXpWvJ_oYT8cB4vzsnJLe3iCwuzj-w6PeYq_JaHmy_CoGoa6nw0FBo-2xLdOPvsLTh_fmYH2xhkaZ-OGQ/s16000/footer_bg.png") no-repeat scroll center 0;
                            width: 100%;
                            height: 266px;
                        }

                        .new_footer_top .footer_bg .footer_bg_one {
                            background: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEia0PYPxwT5ifToyP3SNZeQWfJEWrUENYA5IXM6sN5vLwAKvaJS1pQVu8mOFFUa_ET4JuHNTFAxKURFerJYHDUWXLXl1vDofYXuij45JZelYOjEFoCOn7E6Vxu0fwV7ACPzArcno1rYuVxGB7JY6G7__e4_KZW4lTYIaHSLVaVLzklZBLZnQw047oq5-Q/s16000/volks.gif") no-repeat center center;
                            width: 330px;
                            height: 105px;
                          background-size:100%;
                            position: absolute;
                            bottom: 0;
                            left: 30%;
                            -webkit-animation: myfirst 22s linear infinite;
                            animation: myfirst 22s linear infinite;
                        }

                        .new_footer_top .footer_bg .footer_bg_two {
                            background: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhyLGwEUVwPK6Vi8xXMymsc-ZXVwLWyXhogZxbcXQYSY55REw_0D4VTQnsVzCrL7nsyjd0P7RVOI5NKJbQ75koZIalD8mqbMquP20fL3DxsWngKkOLOzoOf9sMuxlbyfkIBTsDw5WFUj-YJiI50yzgVjF8cZPHhEjkOP_PRTQXDHEq8AyWpBiJdN9SfQA/s16000/cyclist.gif") no-repeat center center;
                            width: 88px;
                            height: 100px;
                          background-size:100%;
                            bottom: 0;
                            left: 38%;
                            position: absolute;
                            -webkit-animation: myfirst 30s linear infinite;
                            animation: myfirst 30s linear infinite;
                        }



                        @-moz-keyframes myfirst {
                          0% {
                            left: -25%;
                          }
                          100% {
                            left: 100%;
                          }
                        }

                        @-webkit-keyframes myfirst {
                          0% {
                            left: -25%;
                          }
                          100% {
                            left: 100%;
                          }
                        }

                        @keyframes myfirst {
                          0% {
                            left: -25%;
                          }
                          100% {
                            left: 100%;
                          }
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

                .panels {

                      height:100vh;
                    width:100%;
                    scroll-snap-type:y mandatory;
                    }

                  .panel {
                    box-shadow:40px red;
                    scroll-snap-align: start;
                    width: 100%;
                    height:100vh;
                    background:rgba(0,0,0,0.25);
                    display:flex;
                    justify-content:center;
                    background:#1d1e22;
                  }

                  .clip {
                        position: sticky; 
                        height:0;
                        background:red;
                        width:100%;
                        top:0;
                        margin-bottom:0;
                    }
                  .tint { 
                    display:block;
                    position:absolute;
                    top:0;
                    left:0;
                    background:rgba(0,0,0,0.1);
                    width:100vw;
                    height:100vh;
                    z-index:2;
                    pointer-events:none;
                  }
                    .video_clip {
                        position: absolute;
                        top:0;
                        left:0;
                        width:100%; 
                        height:100vh;
                        z-index: 1;
                        pointer-events: none;
                        overflow: hidden;
                    }
                    iframe {
                        z-index:1;
                        border:0;
                        width: 100vw;
                        height: 56.25vw; 
                        min-height: 100%;
                        min-width: 177.77vh; 
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                    }

            </style>                     
            </head>


            <body>
            <div class="panels" id="panelContainer">
              <div class="panel one" id="panel_1">
                  <div class="clip">
                      <h2><a>News Analyzer</a></h2><span class="tint"></span>
                      <div class="video_clip">
                        <iframe src="https://player.vimeo.com/video/363666651?&api=1&controls=0&background=1&autoplay=1&loop=1&mute=1" allow="autoplay;"></iframe>
                        </div>			
                  </div>
              </div>
           </div>

            <header>
                <div class="content">
                    <iframe src="https://player.vimeo.com/video/867338027?&api=1&controls=0&background=1&autoplay=1&loop=1&mute=1" allow="autoplay;"></iframe>
                    <hgroup>
                        <h1 style="color:white;">THE NEWS OF OUR TIME</h1>
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
                    <iframe src="https://player.vimeo.com/video/468155263?&api=1&controls=0&background=1&autoplay=1&loop=1&mute=1" allow="autoplay;"></iframe>
                  <form method = 'post' class="entries"> 
                      <div class="inputs">
                            <label>Enter link</label>
                            <input type="text" id="link" name="link" ><br>
                            <label>Enter the following:-<br>
                                        -> div <br>
                                        -> h5  <br>
                                        -> h4  <br>
                                        -> h3  <br>
                                        -> h2  <br>
                                        -> p  
                                    <br> </label>
                            <input type="text" id="custom" name="custom" ><br>
                            <input type="submit" value="submit">
                      </div>
                  </form>
                </div>  

                </center>         


               </section> 





            <footer class="new_footer_area bg_color">
             <div class="new_footer_top">
                    <div class="footer_bg">
                        <div class="footer_bg_one"></div>
                        <div class="footer_bg_two"></div>
                    </div>
            </div>




                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <link rel="preconnect" href="https://fonts.gstatic.com">
                <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Play&display=swap" rel="stylesheet"> 


                <div class="footer">
                <div class="row">
                <a href="#"><i class="fa fa-facebook"></i></a>
                <a href="#"><i class="fa fa-instagram"></i></a>
                <a href="#"><i class="fa fa-youtube"></i></a>
                <a href="#"><i class="fa fa-twitter"></i></a>
                </div>

                <div class="row">
                <ul>
                <li><a href="#">Contact us</a></li>
                <li><a href="#">Our Services</a></li>
                <li><a href="#">Privacy Policy</a></li>
                <li><a href="#">Terms & Conditions</a></li>
                </ul>
                    <ul class="menu">
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/trending/" target="_blank" >Trending News</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/sports/" target="_blank" >Sports News</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/entertainment/" target="_blank">Entertainment</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/technology/mobile-tabs/" target="_blank" >Technology</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/health-wellness/" target="_blank">Health News</a></li>
                      <li class="menu__item"><a class="menu__link" href="https://indianexpress.com/section/business/" target="_blank">Business News</a></li>
                    </ul>
                </div>
                <div class="row">
                Copyright © 2023 - All rights reserved || Designed By: Sachin Pandey 
                </div>
                </div>

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
              <form style=" padding: 16px;width: 16px*20;margin: 0 auto; ">
                    <h3><center><strong style="color:red;">ANALYZED SENTIMENT</strong><center></h3><br>
                    <label for="fname" style=" font-size: $ruler;" ><strong>Today's Date: </strong> {}</label><br>
                    <label for="lname" style="font-size: $ruler;" ><strong>Counter: </strong>{}</label><br>
                    <label for="lname" style="font-size: $ruler;" ><strong>Score: </strong>{}</label><br>
                    <label for="sentiment" style="font-size: $ruler;" ><strong>Sentiment after reading: </strong><strong style="color:red;">{}</strong></label><br><br>
                    <label for="lname" style="font-size: $ruler;" ><strong>Text: </strong>{}</label><br>
              </form>
        </div>
    </body>
    '''.format(d, w, score, sentiment, text)


if __name__ == '__main__':
    app.run(debug=True)
