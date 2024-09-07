from youtube_transcript_api import YouTubeTranscriptApi as yta
from transformers import pipeline
from flask import Flask, request, render_template
app=Flask(__name__)

def get_trans(id):
    url = id.split('=')[1]
    data=yta.get_transcript(url)
    trans=""
    for value in data:
        for key,val in value.items():
            if key=='text':
                trans+=val
    para=trans.splitlines()
    txt=" ".join(para)
    return txt
# texxt=get_trans("aDG1T0kJnd4?si=dxpNPdyZ2qnSNJ7B")
def get_sum(transcript):
    summariser = pipeline('summarization', model="sshleifer/distilbart-cnn-12-6")
    summary = ""
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_id = request.form['video_id']
        transcript = get_trans(video_id)
        summary = get_sum(transcript)
        return render_template('index.html', transcript=transcript, summary=summary)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
