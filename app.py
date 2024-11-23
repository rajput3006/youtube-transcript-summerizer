from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])    
def index():
    output = None
    if request.method == 'POST':
        user_input = request.form['user_in']
        lang = request.form['lang']
        try:
            output = results(user_input, lang)
        except VideoUnavailable:
            output = "The video is unavailable."
    return render_template('index.html', output=output)

def results(user_in, language):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(user_in)
        transcript = transcript_list.find_transcript([language])
        var = transcript.fetch()
        final = returnText(var)
        return final
    except Exception as e:
        return "Error: " + str(e)

def returnText(ls):
    return ' '.join([item['text'] for item in ls])

def u_in(user_input):
    ln = len(user_input)
    fn = ""
    for i in range(0, 100):
        if(user_input[i] == '=' and user_input[i-1] == 'v'):
            for j in range(i+1, 100):
                fn = fn + user_input[j]
    return fn

@app.route('/out')
def out():
    return render_template('out.html')

if __name__ == '__main__':
    app.run(debug=True)