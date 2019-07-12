知乎爬虫介绍：

1.难点在于登陆页面的验证码识别，登录页出现的验证码有：英文字母验证码、点击倒立汉字验证码。
（1）.英语验证码识别相对简单，本项目运用第三方打码平台识别。
（2）.点击倒立汉字验证码识别很复杂，好在github(https://github.com/muchrooms/zheye)上有开源项目可以识别，成功率很高，使用也很简单。
```python
from zheye import zheye
from mouse import move, click
z = zheye()
positions = z.Recognize(r"image/verify_code.gif")

move(positions[0], positions[1])
click()

```
传入倒立汉字验证码图片，识别出倒立汉字的坐标(x, y), 最后模拟鼠标移动、点击完成识别验证。

2.这个过程中有很多坑需要注意：
（1）.打开的浏览器必须是缩放为100%模式，不然识别出来的坐标不正确
（2）. Chrome 浏览器必须保证初始打开时一样，特别是出现下载文件的进度条时，要关闭进度条，以免遮挡住浏览器底部，影响坐标。
（3）. zheye 识别出来的坐标部分Y轴比X轴大，通过观察图片可知，Y轴不可能比X轴大，遇到此情况需要把X、Y轴对调，交换位置。

