from flask import Flask, render_template
from flask import request, make_response
from flask import jsonify
import pyautogui as pg
import pyperclip
import subprocess
from IPTVChannel import *
app = Flask(__name__)

iptv_channel = IPTVChannel()
last_channel_idx = 0
g_m3u8 = []

def response_code_0():
    code = {"code": 0}
    resp = make_response(code)
    resp.headers['Connection'] = 'keep-alive'
    return resp
    
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/mouse')
def mouse():
    return render_template('mouse.html')

@app.route('/iptv')
def iptv():
    return render_template('iptv.html', url=iptv_channel.last())

@app.route('/iptv_control')
def iptv_control():
    subprocess.Popen(['chrome', 'http://localhost:5000/iptv'])
    iptv_channel.getChannels('http://192.168.1.110/media/IPTV-URL/IPTV-fix.m3u')
    if len(iptv_channel.channels) == 0:
        return "channel empty"
    return render_template('iptv_control.html', channels=iptv_channel.channels)

@app.route('/get_m3u8')
def get_m3u8():
    result = ""
    if len(g_m3u8) > 0:
        result = g_m3u8[-1]
        g_m3u8.clear()
        
    return result

@app.route("/prev_channel", methods=['POST'])
def prev_channel():
    url = iptv_channel.prev()
    g_m3u8.append(url)
    return response_code_0()

@app.route("/next_channel", methods=['POST'])
def next_channel():
    url = iptv_channel.next()
    g_m3u8.append(url)
    return response_code_0()

@app.route("/auto_play", methods=['POST'])
def auto_play():
    pg.click(500,500, button="left")
    return response_code_0()

@app.route("/full_screen", methods=['POST'])
def full_screen():
    pg.doubleClick(500, 500)
    return response_code_0()

@app.route("/set_channel", methods=['POST'])
def set_channel():
    value = eval(request.form.get('value'))
    print("value=",value)
    url = iptv_channel.get(value)
    g_m3u8.append(url)
    return response_code_0()

@app.route('/report_scroll', methods=['POST'])
def report_scroll():
    x = eval(request.form.get('dx'))
    y = eval(request.form.get('dy'))
    t = request.form.get('time')
    sign_x = 1
    sign_y = 1
    if x < 0:
        sign_x = -1
    if y < 0:
        sign_y = -1
    #print("dx: {} dy: {} time: {}", x, y, t)
    pg.scroll(round(y*y*sign_y/10))
    #pg.hscroll(round(eval(x))/3)
    return response_code_0()

@app.route('/report_move', methods=['POST'])
def report_move():
    x = eval(request.form.get('dx'))
    y = eval(request.form.get('dy'))
    t = request.form.get('time')
    sign_x = 1
    sign_y = 1
    if x < 0:
        sign_x = -1
    if y < 0:
        sign_y = -1
    #print("dx: {} dy: {} time: {}", x, y, t)
    pg.moveRel(round(x*x*sign_x/10), round(y*y*sign_y/10))
    return response_code_0()

@app.route("/report_right_click", methods=['POST'])
def report_right_click():
    pg.rightClick();
    print("rightClick")
    return response_code_0()

@app.route("/report_tap", methods=['POST'])
def report_tap():
    pg.leftClick()
    print("leftClick")
    return response_code_0()

@app.route("/report_text", methods=['POST'])
def report_text():
    text = request.form.get('text')
    print(text)
    pyperclip.copy(text)
    pg.hotkey('ctrl','v')
    return response_code_0()

@app.route("/report_delete", methods=['POST'])
def report_delete():
    pg.press('backspace')
    return response_code_0()
    
@app.route("/report_enter", methods=['POST'])
def report_enter():
    pg.press('enter')
    return response_code_0()
    
@app.route("/report_quit", methods=['POST'])
def report_quit():
    pg.hotkey('ctrl','w')
    return response_code_0()

    
@app.route("/report_left_down", methods=['POST'])
def report_left_down():
    pg.mouseDown();
    return response_code_0()

@app.route("/report_left_up", methods=['POST'])
def report_left_up():
    pg.mouseUp();
    return response_code_0()

if __name__ == "__main__":
    pg.FAILSAFE=False
    app.run(host='0.0.0.0', port=5000)
