import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
fontprop = FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# 테스트 그래프
plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
plt.title('한글 제목 테스트', fontproperties=fontprop)
plt.xlabel('X축 레이블', fontproperties=fontprop)
plt.ylabel('Y축 레이블', fontproperties=fontprop)
plt.show()
