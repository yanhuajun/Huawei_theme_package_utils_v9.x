#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 
import chardet
import re
import platform
from PIL import Image

isWindows = False

queshipicArr = []

currentProjectFilePath = ''

fileList = ['com.android.contacts' , 'com.android.mms'  ,'com.android.phone' , 'com.android.phone.recorder' , 'com.android.server.telecom' , 'com.android.systemui' ,
	'com.huawei.android.launcher' , 'com.huawei.hwvoipservice'
]


framework_res_hwext_change_v9_v10=[
	{
		'orgin':'<color name="hwtoolbar_background">(.*)</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_appbar_bg_blur">{color}</color>','color':'{orgincolor}00'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="hwtoolbar_background">(.*)</color>',
		'replace':[{'tag':'<color name="emui_toolbar_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_toolbar_bg_blur">{color}</color>','color':'{orgincolor}00'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="navigationbar_emui_light">(.*)</color>',
		'replace':[{'tag':'<color name="emui_navigationbar_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_navigationbar_bg_blur">{color}</color>','color':'{orgincolor}00'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_color_gray_1">(.*)</color>',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_subtab_bg_blur">{color}</color>','color':'{orgincolor}00'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_tips_bg">{color}</color>','color':'#F2D9D9D9'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'#FFFFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_control_normal">{color}</color>','color':'#19000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_toast_bg">{color}</color>','color':'#F2D9D9D9'}],
		'target':'',
		'color':''
	},
]
framework_res_hwext_change_v91_v10=[
	# 默认颜色则直接修改  非默认颜色保持不变

	# 颜色必须保持一致开始 
	{
		'orgin':'<color name="emui_appbar_bg">#F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>','color':'#E6FFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_appbar_bg">(.*)</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>','color':'{color}'}],
		'target':'framework_res_hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},
	
	{
		'orgin':'<color name="emui_appbar_bg_blur">(.*)</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg_blur">{color}</color>','color':'{color}'}],
		'target':'framework_res_hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},
	{
		'orgin':'<color name="emui_appbar_bg_blur">#80F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg_blur">{color}</color>','color':'#FF000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_toolbar_bg">#FF262626</color>',
		'replace':[{'tag':'<color name="emui_toolbar_bg">{color}</color>','color':'#F2FAFAFA'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_toolbar_bg_blur">#80262626</color>',
		'replace':[{'tag':'<color name="emui_toolbar_bg">{color}</color>','color':'#F2FAFAFA'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_appbar_bg">#F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>','color':'#E6FFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_appbar_bg_blur">#80F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg_blur">{color}</color>','color':'#FF000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_navigationbar_bg">#FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_navigationbar_bg">{color}</color>','color':'#F2FFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_navigationbar_bg_blur">#80FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_navigationbar_bg_blur">{color}</color>','color':'#ff000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_subtab_bg">#f0f0f0</color>',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>','color':'#E6FFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_subtab_bg_blur">#80f0f0f0</color>',
		'replace':[{'tag':'<color name="emui_subtab_bg_blur">{color}</color>','color':'#ff000000'}],
		'target':'',
		'color':''
	},
	# 颜色必须保持一致   结束

	{
		'orgin':'<color name="emui_color_tips_bg">#FF666666</color>',
		'replace':[{'tag':'<color name="emui_color_tips_bg">{color}</color>','color':'#F2D9D9D9'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_color_bg">#ffffff</color>',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'#FFFFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_control_normal">{color}</color>','color':'#19000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_toast_bg">{color}</color>','color':'#F2D9D9D9'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_color_divider_horizontal">#33FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_color_divider_horizontal">{color}</color>','color':'#33000000'}],
		'target':'',
		'color':''
	},

	# 切换至.9图
	{
		'orgin':'<color name="emui_color_gray_4">#cacaca</color>',
		'replace':[{'tag':'','color':''}],
		'target':'',
		'color':''
	},

	{
		'orgin':'<color name="emui_color_fg">#000000</color>',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'#FFFFFFFF'}],
		'target':'',
		'color':''
	},
	
	{
		'orgin':'<color name="emui_color_fg">(.*)</color>',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'{orgincolor}'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_connected">{color}</color>','color':'#41ba41'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_accent">#007dfe</color>',
		'replace':[{'tag':'<color name="emui_accent">{color}</color>','color':'#FF007DFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_functional_blue">#005bba</color>',
		'replace':[{'tag':'<color name="emui_functional_blue">{color}</color>','color':'#007DFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_switch_bg_on">#007dfe</color>',
		'replace':[{'tag':'<color name="emui_switch_bg_on">{color}</color>','color':'#007DFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_progress">#808080</color>',
		'replace':[{'tag':'<color name="emui_progress">{color}</color>','color':'#4D4D4D'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_control_hightlight">(.*)</color>',
		'replace':[{'tag':'<color name="emui_functional_blue">{color}</color>','color':'{orgincolor}'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_spinner_icon">(.*)</color>',
		'replace':[{'tag':'<color name="emui_color_spinner_icon">{color}</color>','color':'{orgincolor}'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_appbar_icon">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_appbar_icon">{color}</color>','color':'#E6000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_appbar_icon_pressed">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_appbar_icon_pressed">{color}</color>','color':'#E6000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_appbar_title">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_appbar_title">{color}</color>','color':'#E6000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_toolbar_icon">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_icon">{color}</color>','color':'#E6000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_toolbar_icon_pressed">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_icon_pressed">{color}</color>','color':'#E6000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_toolbar_text">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_text">{color}</color>','color':'#E6000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_toolbar_text_pressed">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_text_pressed">{color}</color>','color':'#E6000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_subtab_text_off">(.*)</color>',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_off">{color}</color>','color':'{orgincolor}'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_subtab_text_off">(.*)</color>',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_off">{color}</color>','color':'{orgincolor}'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_bottombar_icon_off">#FFFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_bottombar_icon_off">{color}</color>','color':'#99000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_bottombar_text_off">#FFFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_bottombar_text_off">{color}</color>','color':'#99000000'}],
		'target':'',
		'color':''
	},

	# emui_black_color_alpha_30 已删除 ,切换至.9图
	{
		'orgin':'<color name="emui_text_hint">#191919</color>',
		'replace':[{'tag':'','color':''}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_bottombar_text_off">#FFFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_bottombar_text_off">{color}</color>','color':'#99000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_icon_tertiary">#191919</color>',
		'replace':[{'tag':'<color name="emui_icon_tertiary">{color}</color>','color':'#4D000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_secondary">(.*)</color>',
		'replace':[{'tag':'<color name="emui_primary">{color}</color>','color':'{orgincolor}'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_appbar_subtitle">{color}</color>','color':'#99000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_accent">#007dfe</color>',
		'replace':[{'tag':'<color name="emui_accent">{color}</color>','color':'#007dff'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_fastscroll_lable_bg">#e4e4e4</color>',
		'replace':[{'tag':'<color name="emui_fastscroll_lable_bg">{color}</color>','color':'#E6E6E6'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="switch_off_disable_emui">#4De4e4e4</color>',
		'replace':[{'tag':'<color name="switch_off_disable_emui">{color}</color>','color':'#0E000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_checkbox_boxedge">#4D000000</color>',
		'replace':[{'tag':'<color name="emui_checkbox_boxedge">{color}</color>','color':'#191919'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_switch_outline_off">#4DFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_switch_outline_off">{color}</color>','color':'#B3B3B3'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_switch_bg_off">#FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_switch_bg_off">{color}</color>','color':'#4D000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'<color name="emui_white_bg">#e4e4e4</color>',
		'replace':[{'tag':'<color name="emui_white_bg">{color}</color>','color':'#FFFFFF'}],
		'target':'',
		'color':''
	},

	# progress_primary_emui.9.png  , progress_bg_emui.9.png   亮度调整 条  ,26*74
]

launcher_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="ic_home_checkbox_off_center_color">{color}</color>' , 'color':'#FFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="ic_home_checkbox_off_rim_color">{color}</color>' , 'color':'#000000'}],
		'target':'',
		'color':''
	},
	
]

contacts_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="ic_home_checkbox_off_center_color">{color}</color>' , 'color':'#FFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="ic_home_checkbox_off_rim_color">{color}</color>' , 'color':'#000000'}],
		'target':'',
		'color':''
	},

	# 联系人/收藏/新建按钮背景色
	# 背景颜色:
	# <color name="hwfab_bg">#007DFF</color>
	# 背景按压颜色:
	# <color name="hwfab_pressed">#0070E5</color>
	# 图标背景投影色:
	# <color name="hwfab_shadow_start">#4D00B0FF</color>
	# <color name="hwfab_shadow_end">#4DFF00D0</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_bg">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_pressed">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_shadow_start">{color}</color>' , 'color':'{color}FF'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_shadow_end">{color}</color>' , 'color':'{color}D0'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},

	# 拨号/拨号盘展开收起悬浮按钮背景色
	# 背景颜色:
	# nomal状态
	# <color name="dial_fab_backgrounp">#41ba41</color>
	# pressed状态
	# <color name="dial_fab_backgrounp_pressed">#41ba41</color>
	# focused状态
	# <color name="dial_fab_backgrounp_focue">#41ba41</color>
	# 图标背景投影色:
	# <color name="dial_hwfab_shadow_start">#4D00B0FF</color>
	# <color name="dial_hwfab_shadow_end">#4DFF00D0</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_fab_backgrounp">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_fab_backgrounp_pressed">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_fab_backgrounp_focue">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_hwfab_shadow_start">{color}</color>' , 'color':'{color}FF'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_hwfab_shadow_end">{color}</color>' , 'color':'{color}D0'}],
		'target':'framework-res-hwext',
		'color':'<color name="primary_emui_light">(.*)</color>'
	},

	# 拨号图标
	# 图标背景色nomal状态,引用 framework-res-hwext:
	# <color name="emui_color_connected">#41ba41</color>
	# 图标背景色pressed状态,
	# <color name="contact_svg_icon_base_green_color_a">#20A934</color>
	# 图标颜色,引用 framework-res-hwext:
	# <color name="emui_color_fg_inverse">#ffffff</color>
	# 图标不可用颜色,引用 framework-res-hwext:
	# <color name="emui_color_fg_inverse">#ffffff</color>叠加38%不透明度
	# 图标按压色:
	# <color name="contact_svg_icon_base_grey_color_c">#D6D6D6</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_connected">{color}</color>' , 'color':'#41ba41'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="contact_svg_icon_base_green_color_a">{color}</color>' , 'color':'#20A934'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_fg_inverse">{color}</color>' , 'color':'#ffffff'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_fg_inverse">{color}</color>' , 'color':'#ffffff'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="contact_svg_icon_base_grey_color_c">{color}</color>' , 'color':'#D6D6D6'}],
		'target':'',
		'color':''
	},


	{
		'orgin':'',
		'replace':[{'tag':'<color name="bottom_tab_bg">{color}</color>' , 'color':'#ffffff'}],
		'target':'',
		'color':''
	},

	# 拨号/联系人、收藏主界面/新建按钮（可保留默认状态）
	# 拨号/悬浮图标颜色
	# <color name="hwfab_icon_start">#00B0FF</color>
	# <color name="hwfab_icon_end">#FF00D0</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_icon_start">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="emui_primary">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_icon_end">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="emui_primary">(.*)</color>'
	},

	# 联系人首次启动条幅背景色
	# <color name="tips_and_divider_color">#FFFFFFFF</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="tips_and_divider_color">{color}</color>' , 'color':'#FFFFFFFF'}],
		'target':'',
		'color':''
	},

	# <color name="hwsubtab_emui_color_bg">#ffffff</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_emui_color_bg">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="emui_color_fg">(.*)</color>'
	},

	# 选中的页签文字颜色:<color name="hwsubtab_emui_subtab_text_on">#007dff</color>
	# 下划线图标颜色:<color name="hwsubtab_indicator_color">#007dff</color>
	# 未选中的页签文字颜色:<color name="hwsubtab_emui_subtab_text_off">#191919</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_on">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="emui_control_hightlight">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_indicator_color">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="emui_control_hightlight">(.*)</color>'
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_off">{color}</color>' , 'color':'{color}'}],
		'target':'framework-res-hwext',
		'color':'<color name="emui_primary">(.*)</color>'
	},

	# svg图片,即电话或者摄像头图标的颜色:<color name="hicall_recent_call_type_image">#FFFFFF</color>
	# 灰色背景颜色:  引用 framework-res-hwext:
	# <color name="emui_primary">#191919</color>叠加  38%不透明
	# 灰色背景周围白色描边颜色:  引用 framework-res-hwext:
	# <color name="emui_color_bg">#ffffff</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hicall_recent_call_type_image">{color}</color>' , 'color':'#FFFFFF'}],
		'target':'',
		'color':''
	},

	# 新增.9图
	# 图标背景资源:daier_call_btn_normal.png
	# 图标背景按压资源:daier_call_btn_press.png
	# dialpad_background_drawable.9.png 拨号键盘中间间隔 ,无固定尺寸
	# header_background4.9.png
]

# hwvoipservice 新增包 直接用官方包替代
hwvoipservice_framework_res_hwext_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_appbar_bg_blur">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwtoolbar_background">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_toolbar_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_toolbar_bg_blur">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_navigationbar_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_navigationbar_bg_blur">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="navigationbar_emui_light">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_subtab_bg_blur">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_tips_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
]

hwvoipservice_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="compose_bottom_layout_background">{color}</color>' , 'color':'{color}'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="embedded_text_editor_background">{color}</color>' , 'color':'{color}'}],
		'target':'../com.android.mms',
		'color':'<color name="message_editor_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="msg_text_body_color">{color}</color>' , 'color':'#ffffff'}],
		'target':'com.android.mms/framework-res-hwext',
		'color':'<color name="hwtoolbar_background">(.*)</color>'
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="msg_pop_incoming_bg_color">{color}</color>' , 'color':'FFFFFFCC'}],
		'target':'',
		'color':''
	},	
	{
		'orgin':'',
		'replace':[{'tag':'<color name="msg_pop_send_bg_color">{color}</color>' , 'color':'#000000'}],
		'target':'',
		'color':''
	},	

]

mms_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="color_gray_one">{color}</color>' , 'color':'{color}'}],
		'target':'',
		'color':'<color name="fab_new_message_bg">(.*)</color>'
	},

	{
		'orgin':'',
		'replace':[{'tag':'<color name="messaeg_pop_text_color_send_sms_theme_adapter">{color}</color>' , 'color':'#ffffff'}],
		'target':'',
		'color':''
	},


	# 新增.9图
	# <!-- 待发区信息气泡背景颜色 -->
	# <!-- 会话界面 发送消息的泡泡的背景色 -->
	# <!-- 会话界面 接收消息的泡泡的背景颜色 -->
	# <!-- 发送加密短信发送气泡背景颜色 -->
	# <!-- 增强信息发送气泡背景颜色 -->
	# 具体
	# message_attachment_preview_bg	"172x102
	# 可以不固定,保证全区域可显示"	"待发区气泡背景
	# 如有方向,注意镜像"
	# "
	# message_location_pop_send_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 发送的地理位置气泡背景,圆角30px
	# 如有方向,注意镜像"
	# "
	# message_pop_favorite_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 收藏的发送的短信气泡背景
	# 如有方向,注意镜像"
	# "
	# message_pop_incoming_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 接收信息气泡、收藏的接收气泡背景
	# 如有方向,注意镜像"
	# "
	# message_pop_rcs_favorite_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 收藏的发送的rcs气泡背景
	# 如有方向,注意镜像"
	# "
	# message_pop_rcs_image_bg_long_press"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 四圆角蒙版气泡背景,需要有透明度,否则看不清短信文字,圆角30px
	# 如有方向,注意镜像"
	# "
	# message_pop_rcs_receive_bg_long_press"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 接收气泡蒙版气泡背景,需要有透明度,否则看不清短信文字
	# 如有方向,注意镜像"
	# "
	# message_pop_rcs_send_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# rcs发送气泡气泡背景
	# 如有方向,注意镜像"
	# "
	# message_pop_rcs_send_bg_long_press"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 发送气泡蒙版气泡背景,需要有透明度,否则看不清短信文字
	# 如有方向,注意镜像"
	# "
	# message_pop_send_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 短信发送出去之后气泡背景
	# 如有方向,注意镜像"
	# "
	# message_slide_pop_incoming_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 彩信幻灯片带图片接收气泡背景,圆角30px
	# 如有方向,注意镜像"
	# "
	# message_slide_pop_send_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 彩信幻灯片带图片发送气泡背景
	# 如有方向,注意镜像"
	# "
	# encrypted_message_pop_send_bg"	"172x102
	# 可以不固定,保证全区域可显示"	"
	# 加密短信气泡背景
	# 如有方向,注意镜像"


	# <!--增强信息 按住说话button文字颜色 -->
	# 背景引用 framework-res-hwext 切图:
	# button_big_bg_stroked.9.png（大）
	# button_small_bg_stroked.9.png（小）
	# button_big_bg_stroked_pressed.9.png（大）
	# button_small_bg_stroked_pressed.9.png（小）
	# button_big_bg_stroked_disable.9.png(大)
	# button_small_bg_stroked_disable.9.png(小)


	# 新建短信按钮颜色
	{
		'orgin':'',
		'replace':[{'tag':'<color name="mms_color_primary_dark">{color}</color>' , 'color':'#ffffff'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="messaeg_pop_text_color_send_rcs_theme_adapter">{color}</color>' , 'color':'#242424'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="message_pop_send_bg_color">{color}</color>' , 'color':'#26c73d'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="messaeg_pop_text_color_send_sms_theme_adapter">{color}</color>' , 'color':'#242424'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="messaeg_pop_text_color_send_rcs_theme_adapter">{color}</color>' , 'color':'#242424'}],
		'target':'',
		'color':''
	},

	# <!-- 智能短信 弹框背景-->
	# <color name="duoqu_rcs_url_bg_color">#FFFFFF</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="duoqu_rcs_url_bg_color">{color}</color>' , 'color':'#FFFFFF'}],
		'target':'',
		'color':''
	},
]

systemui_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="qs_customize_background_color1">{color}</color>' , 'color':'#FFFFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="notification_background_color_without_alpha">{color}</color>' , 'color':'#FFFFFFFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="notification_button_pressed_bg_color">{color}</color>' , 'color':'#0d000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="notification_button_pressed_bg_color">{color}</color>' , 'color':'#0d000000'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="qs_tile_tint_on">{color}</color>' , 'color':'#FFFFFF'}],
		'target':'',
		'color':''
	},

	# 背景引用 framework-res-hwext 切图:
	# button_big_bg_stroked.9.png（大）
	# button_small_bg_stroked.9.png（小）
	# button_big_bg_stroked_pressed.9.png（大）
	# button_small_bg_stroked_pressed.9.png（小）
	# button_big_bg_stroked_disable.9.png(大)
	# button_small_bg_stroked_disable.9.png(小)


	{
		'orgin':'',
		'replace':[{'tag':'<color name="volume_line_color">{color}</color>' , 'color':'#333333'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="volume_image_color">{color}</color>' , 'color':'#FF007DFF'}],
		'target':'',
		'color':''
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="volume_unfocus">{color}</color>' , 'color':'#FF007DFF'}],
		'target':'',
		'color':''
	},

	# 增加.9图  , ic_seekbar_thumb.png	96×96	音量控制滑块
]

phone_normalConfig_v91_v10 = []


recorder_normalConfig_v91_v10 = []


icons_normalConfig_v91_v10 = [
	# 图标增加 


	# "com.android.calendar
	# com.huawei.calendar"	日历（静态）	192×192

	# "com.android.contacts
	# com.huawei.contacts"	联系人	192×192

	# "com.android.email
	# com.huawei.email"	电子邮件	192×192

	# "com.example.android.notepad
	# com.huawei.notepad"	备忘录	192×192

	{'com.android.calendar':'com.huawei.calendar'},
	{'com.android.contacts':'com.huawei.contacts'},
	{'com.android.email':'com.huawei.email'},
	{'com.example.android.notepad':'com.huawei.notepad'},
	
]
dynamic_icons = [
	
	# ic_deskclock_dial	动态模拟时钟背板	192×192	"icons\dynamic_icons\com.huawei.deskclock"
	# ic_deskclock_hour	动态模拟时钟时针	18×192	
	# ic_deskclock_minute	动态模拟时钟分针	18×192	
	# ic_deskclock_second	动态模拟时钟秒针	18×192	
	'icons/dynamic_icons/com.huawei.deskclock/ic_deskclock_dial.png',
	'icons/dynamic_icons/com.huawei.deskclock/ic_deskclock_hour.png',
	'icons/dynamic_icons/com.huawei.deskclock/ic_deskclock_minute.png',
	'icons/dynamic_icons/com.huawei.deskclock/ic_deskclock_second.png',
]


normalConfig_dic = {
	'contacts_normalConfig_v91_v10':contacts_normalConfig_v91_v10,
	'mms_normalConfig_v91_v10':mms_normalConfig_v91_v10,
	'phone_normalConfig_v91_v10':phone_normalConfig_v91_v10,
	'recorder_normalConfig_v91_v10':recorder_normalConfig_v91_v10,
	'systemui_normalConfig_v91_v10':systemui_normalConfig_v91_v10,
	'launcher_normalConfig_v91_v10':launcher_normalConfig_v91_v10,
	'hwvoipservice_normalConfig_v91_v10':hwvoipservice_normalConfig_v91_v10
}

dot9picList = [
#  constacts
	{'input':'constacts/daier_call_btn_normal.png','output':'com.android.contacts/framework-res-hwext/res/drawable-xxhdpi/daier_call_btn_normal.png',
	'color':'<color name="primary_emui_light">(.*)</color>',
	'defaultcolor':'#ffffff',
	'target':'framework-res-hwext'},

	{'input':'constacts/daier_call_btn_press.png','output':'com.android.contacts/framework-res-hwext/res/drawable-xxhdpi/daier_call_btn_press.png',
	'color':'<color name="primary_emui_light">(.*)</color>',
	'defaultcolor':'#ffffff',
	'target':'framework-res-hwext'},

	{'input':'constacts/dialpad_background_drawable.9.png','output':'com.android.contacts/res/drawable-xxhdpi/dialpad_background_drawable.9.png',
	'color':'<color name="primary_emui_light">(.*)</color>',
	'defaultcolor':'#ffffff',
	'target':'framework-res-hwext'},

	{'input':'constacts/header_background4.9.png','output':'com.android.contacts/res/drawable-xxhdpi/header_background4.9.png',
	'color':'<color name="primary_emui_light">(.*)</color>',
	'defaultcolor':'#ffffff',
	'target':'framework-res-hwext'},


# sms


	{'input':'mms/message_slide_pop_incoming_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_slide_pop_incoming_bg.9.png',
	'color':'<color name="message_pop_incoming_bg_color">(.*)</color>',
	'defaultcolor':'#ffffff',
	'target':''},

	{'input':'mms/message_pop_incoming_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_pop_incoming_bg.9.png',
	'color':'<color name="message_pop_incoming_bg_color">(.*)</color>',
	'defaultcolor':'#ffffff',
	'target':''},


	{'input':'mms/message_location_pop_send_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_location_pop_send_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},

	{'input':'mms/message_pop_rcs_favorite_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_pop_rcs_favorite_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},

	{'input':'mms/message_pop_rcs_send_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_pop_rcs_send_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},


	{'input':'mms/encrypted_message_pop_send_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/encrypted_message_pop_send_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},

	{'input':'mms/message_attachment_preview_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_attachment_preview_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},

	{'input':'mms/message_pop_favorite_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_pop_favorite_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},

	{'input':'mms/message_pop_send_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_pop_send_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},

	{'input':'mms/message_slide_pop_send_bg.9.png','output':'com.android.mms/res/drawable-xxhdpi/message_slide_pop_send_bg.9.png',
	'color':'<color name="message_pop_send_bg_color_theme_adapter">(.*)</color>',
	'defaultcolor':'#000000',
	'target':''},

]

# 查询所有配置文件位置列表 
def listConfigFileArray():
	frameworkResHwextConfigFilePathList = []
	normalConfigFilePathList = []
	retObj = {}
	for index in range(len(fileList)):
		fileItem = fileList[index]
		frameworkResHwextConfigFilePath = os.path.join(currentProjectFilePath,fileItem , "framework-res-hwext" , "theme.xml")
		# print("frameworkResHwextConfigFilePath:%s(%d)" %(frameworkResHwextConfigFilePath ,index) )
		frameworkResHwextConfigFilePathList.append(frameworkResHwextConfigFilePath)
		normalConfigFilePath = os.path.join(currentProjectFilePath,fileItem , "theme.xml")
		# print("normalConfigFilePath:%s(%d)" % (normalConfigFilePath ,index) )
		normalConfigFilePathList.append(normalConfigFilePath)
	retObj['frameworkResHwextConfigFilePathList'] = frameworkResHwextConfigFilePathList
	retObj['normalConfigFilePathList']  = normalConfigFilePathList
	# print retObj;
	return retObj;

def checkFileExists(configFileDic):
	frameworkResHwextConfigFilePathList = configFileDic['frameworkResHwextConfigFilePathList']
	normalConfigFilePathList = configFileDic['normalConfigFilePathList']
	delList = []
	for index in range(len(frameworkResHwextConfigFilePathList)):		
		path = frameworkResHwextConfigFilePathList[index]
		if not os.path.exists(path):
			print('path:%s,not exists' % path)
			delList.append(path)
	for index in delList:
		frameworkResHwextConfigFilePathList.remove(index)

	delList = []
	for index in range(len(normalConfigFilePathList)):		
		path = normalConfigFilePathList[index]
		if not os.path.exists(path):
			print('path:%s,not exists' % path)
			delList.append(path)
	for index in delList:
		normalConfigFilePathList.remove(index)


	return configFileDic

def doTransform( filePath  , configParam ):
	if len(configParam) == 0:
		return 
	if isWindows:
		filePath = filePath.replace('/','\\',99)
	print 'config file path:' 
	print filePath
	print 'the replace rule :' 
	print configParam

	print 'load config file content ...'
	configFileContent = open(filePath).read()
	print configFileContent
	print 'load the replace rule ...'
	if filePath.find('com.android.mms')> 0 and filePath.find('framework-res-hwext') < 0:
		configFileContent = configFileContent.replace('</hwthemes>','')
	else:
		configFileContent = configFileContent.replace('</resources>','')
	for item in configParam:
		color = ''
		
		if item['orgin'] == '':
			print '----------'
			print 'direct replace :'

			if item['color'] != None and item['color'] != '' :
				print 'need to find orgincolr to replace ...'
				print 'find:' + item['color']
				# color = getOrginColorFromConfig('',configFileContent , item['color']  ,'')
				orginConfigFilePath = os.path.join(filePath.replace('framework-res-hwext\\theme.xml' if isWindows else 'framework-res-hwext/theme.xml'  ,'').replace('\\theme.xml' if isWindows else '/theme.xml' , ''),item['target'],'theme.xml')
				print 'from:%s, start findding...' % (orginConfigFilePath)
				color = getOrginColorFromConfig(orginConfigFilePath,'' , item['color']  ,'')
				print 'find the match color' + color

			for param in item['replace']:
				print 'find :%d' % param['color'].find('{color}') 
				if param['color'].find('{color}') < 0 :
					print 'can not find the color tag in replaceStr   ,color change to :' + param['color'] 
					color = param['color']
				print 'replace item :color -->' + param['color'] + '|||tag:' + param['tag'] + ',color:' + color
				replaceStr =  param['tag'].replace('{color}',color)
				print 'preadd ' + replaceStr + ',check if exists...'
				if configFileContent.find(replaceStr) > 0:
					print 'exists' 
				else:
					print 'not exists , add ...'
					configFileContent+="\n\t<!-- hwv91-v10 autoadd --> \n\t" +replaceStr + "\n" 
					
			print '----------'
		else:
			print '----------'
			for param in item['replace']:
				print 'find ' + item['orgin'] + 'and replace '
				matchObj = re.search(item['orgin'] , configFileContent )
				# print matchObj
				color = ''
				replaceStr = ''
				if matchObj == None:
					print 'do not find the replace str , continue ...'
					continue
				else:
					print 'finded ' + matchObj.group()
					if item['orgin'].find('(.*)') > 0 :
						color = matchObj.group(1)
						print 'find the orgincolor :' + color
				# print '将做如下替换:' + param['tag']
				if param['tag'].find('{color}') > 0:
					color = param['color'].replace('{orgincolor}' , color)
					replaceStr = param['tag'].replace('{color}' , color)
				else:
					replaceStr = param['tag']
				print 'will replce:' + replaceStr
				if configFileContent.find(replaceStr) > 0:
					print 'exists ,do not replace '
				else:
					print 'not exists  , add...'
					configFileContent+="\n\t<!-- hwv91-v10 autoreplace --> \n\t" +replaceStr + "\n" 
				
			print '----------'
	if filePath.find('com.android.mms')> 0 and filePath.find('framework-res-hwext') < 0:
		configFileContent+="\n</hwthemes>\n"
	else:
		configFileContent+="\n</resources>\n"
	print configFileContent
	open(filePath , 'w').write(configFileContent)
	print 'prepare write to  file , the path :' + filePath
		

def checkIcons():
	global queshipicArr
	print 'check icons.....'
	for item in icons_normalConfig_v91_v10:
		for key in item:
			print 'check kv, key:' + key + ' ,value:' + item[key]
			filepath1 = os.path.join(currentProjectFilePath , "icons" , key + '.png')
			filepath2 = os.path.join(currentProjectFilePath , "icons" , item[key] + '.png')
			if os.path.exists(filepath1) and os.path.exists(filepath2):
				print 'exists , do not need add'
			else:
				print 'not exists , need add '
				print filepath1
				print filepath2
				if os.path.exists(filepath1) :
					if isWindows:
						command =  'xcopy \'' + filepath1 + '\' ' + filepath2+ '\' /Y'
						print 'command:' + command
						os.system(command)
					else:
						command =  'cp \'' + filepath1 + '\' \'' + filepath2+ '\' /Y'
						print 'command:' + command
						os.system(command)
					print 'add finish , from' + filepath1 + 'to' + filepath2
					continue
				if os.path.exists(filepath2) :
					if isWindows:
						command = 'xcopy \'' + filepath2 + '\' \'' + filepath1 + '\' /Y'
						print 'command:' + command
						os.system(command)
					else:
						command = 'cp \'' + filepath2 + '\' \'' + filepath1+ '\' /Y'
						print 'command:' + command
						os.system(command)
					print 'add finish ,from ' + filepath2 + 'to' + filepath1

					continue
				

	print 'check dynamic clock icons.....'
	for item in dynamic_icons:
		if  isWindows:
			item = item.replace('/','\\',99)
		tmpPath = os.path.join(currentProjectFilePath , item ) 
		if not os.path.exists(tmpPath):	
			print 'need add :' + tmpPath
			queshipicArr.append(tmpPath)

	# print '复制dynamic_icons...'



def mkdir(path):
    if not os.path.isdir(path):
        mkdir(os.path.split(path)[0])
    else:
        return
    os.mkdir(path)

def checkdot9pic():
	for item in dot9picList:
		inputFilePath = os.path.join(os.getcwd(),item['input'])
		outFilePath = os.path.join(currentProjectFilePath , item['output'] )
		if not os.path.exists(inputFilePath):
			print 'template dot9 file error , path:%s' % inputFilePath
			continue
		if os.path.exists(outFilePath):
			print 'dot9 file exists  path:%s , continue...' %(  outFilePath )
			continue

		arr = outFilePath.split('/')
		tmpPath = ''
		if isWindows:
			tmpPath = '\\' + arr[len(arr)-1]
		else:
			tmpPath = '/' + arr[len(arr)-1]
		tmpPath = outFilePath.replace(tmpPath  ,'');
		if not os.path.exists(tmpPath) :
			mkdir(tmpPath)
		if isWindows:
			inputFilePath = inputFilePath.replace('/','\\',99)
			outFilePath = outFilePath.replace('/','\\',99)
		color = getOrginColorFromConfig(os.path.join(currentProjectFilePath , item['output'].split('/')[0], item['target'] ,'theme.xml')  ,'', item['color'] , item['defaultcolor'])
		changeDot9PngColor(inputFilePath  ,outFilePath , Hex_to_RGB(color))


def getOrginColorFromConfig( filePath ,fileContent,  colorPatten  , defaultcolor):
	color = defaultcolor
	if color == '':
		color = '#ffffff'
	if filePath == '' and fileContent == '' :
		return color
	if filePath != '' and fileContent == '' and not os.path.exists(filePath):
		return color
	if filePath == '' and fileContent == '':
		return color 
	if colorPatten == '' :
		return color
	content = ''
	if filePath != '':
		content = open(filePath).read()
	if fileContent != '':
		content = fileContent
	if content == '' :
		return color
	print 'colorPatten:' + colorPatten
	matchObj = re.search(r''+colorPatten , content )
	if matchObj == None:
		return color
	color = matchObj.group(1)
	print 'color:' + color
	return color 



 
# RGB格式颜色转换为16进制颜色格式
def RGB_to_Hex(rgb):
	RGB = rgb.split(',')            # 将RGB格式划分开来
	color = '#'
	for i in RGB:
		num = int(i)
		# 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制,以字符串形式表示
		color += str(hex(num))[-2:].replace('x', '0').upper()
	print(color)
	return color
 
 
# 16进制颜色格式颜色转换为RGB格式
def Hex_to_RGB(hex):
	r = int(hex[1:3],16)
	g = int(hex[3:5],16)
	b = int(hex[5:7],16)
	rgb = str(r)+','+str(g)+','+str(b)
	print(rgb)
	return rgb


def changeDot9PngColor(inputPic , outputPic ,afterColor):
	outputPic = os.path.join(currentProjectFilePath , 'com.android.mms\\res\\drawable-xxhdpi','test.png')
	# if isWindows:
	# 	arr = outputPic.split('\\')
	# 	outputPic = outputPic.replace(arr[len(arr) -1] , '\'' + arr[len(arr) -1] + '\'')
	# else:
	# 	outputPic.split('/')
	# 	outputPic = outputPic.replace(arr[len(arr) -1] , '\'' + arr[len(arr) -1] + '\'')
	img = Image.open(inputPic) 
	imageWidth = img.width 
	imageHeight = img.height
	print 'imgwidth:%s , imgheight:%s' %(imageWidth, imageHeight);
	
	for i in xrange(imageWidth):
		for j in xrange(imageHeight):
			r,g,b,a= img.getpixel((i,j))
			if a == 0:
				continue
			b=int(afterColor.split(',')[2])
			g=int(afterColor.split(',')[1])
			r=int(afterColor.split(',')[0])
			img.putpixel((i,j), (r,g,b,a)) 
	if imageWidth <=20 and imageHeight <=20:
		print 'saving image file ,inputfile: %s , outputfile:%s' %(  inputPic , outputPic )

		if isWindows:
			# open(outputPic,'w').write('')
			# os.system('touch ' + outputPic )
			img.save(outputPic ,'PNG' ,optimize=1)
		else:
			img.save(outputPic)
		# img.show()
		return 

	img2 = Image.new('RGBA',(imageWidth + 1,imageHeight +1)  ,(0,0,0))
	box1 = (0,0,imageWidth,imageHeight)
	region = img.crop(box1)
	img2.paste(region,(1,1))

	for i in xrange(imageWidth + 1):
		for j in xrange( imageHeight + 1):
			# print 'i:%d , j:%d' % (i,j)
			if i == 0 or i == imageWidth or j ==0 or j == imageHeight:
				if imageWidth > 20 and imageHeight > 20 and ( (i == imageWidth/2 and j == 0) or (i == 0 and j == imageHeight/2) or ( (i >imageWidth/6 and i < imageWidth / 6 * 5) and j == imageHeight) or ( i == imageWidth and j > imageHeight/10 and j< imageHeight/10*9 ) ) :
					b = 0
					g = 0
					r = 0
					a = 255
				else:
					b = 0
					g = 0
					r = 0
					a = 0
				img2.putpixel((i,j), (r,g,b,a)) 

	print 'saving image file ,created new image2  outputfile:%s' %(   outputPic )
	if isWindows:
		# os.system('touch ' + outputPic )
		img2.save(outputPic ,'PNG' ,optimize=1)	
	else:
		img2.save(outputPic)
	# img2.save(outputPic)
	# img2.show()

def udpateSystemUi():
	print 'delete hw_recents_close_all.png'
	if isWindows:
		os.system('')

	print 'delete hw_recents_close_all_press.png'


def updateLauncher():
	productLauncherPath = os.path.join(currentProjectFilePath , 'com.huawei.android.launcher' ,'res' , 'drawable-xxhdpi') 
	tempLauncherPath = os.path.join(os.getcwd() , 'launcher' )
	command = ''
	if not isWindows :
		command = 'cp ' + tempLauncherPath + '/*.* ' + productLauncherPath + '/' 
	else:
		command = 'xcopy ' + tempLauncherPath + '\\*.* ' + productLauncherPath + '\\ /Y'
	print 'updateLauncher , command:' + command
	os.system(command);

def updateThemeDesc():
	descFilePath = os.path.join(currentProjectFilePath , 'description.xml');
	content = open(descFilePath).read()
	matchObj = re.search(r'<version>(.*)</version>' , content )
	versionStr = matchObj.group()
	print 'version:' + versionStr
	content = content.replace(versionStr , '<version>10.0.0</version>')
	print 'content after change' + content 
	open(descFilePath,'w').write(content)

# start 
# print '输入参数列表:' 
if len(sys.argv) > 1:
	for index in range(len(sys.argv)):
		if index == 1:
			currentProjectFilePath = sys.argv[index]
else:
	currentProjectFilePath = os.getcwd()
print 'currentProjectFilePath :' + currentProjectFilePath
print '\n'
# 判断是否windows
print  'now system version:' + platform.system()
if platform.system() == 'Windows' or platform.system() == 'windows':
	isWindows = True

if isWindows:
	print 'windows env'
else:
	print 'not windows env'

print '============== from currentProjectFilePath  , find the config file and replace them =============='
configFileDic = listConfigFileArray();
print '============== check the file if exists  ,if not  ,need default file , or just remove  ,=============='
configFileDic = checkFileExists(configFileDic)
print '============== check the file if exists  ,if not  ,need default file , or just remove  ,=============='

if len(configFileDic['normalConfigFilePathList']) == 0 or len(configFileDic['frameworkResHwextConfigFilePathList']) == 0:
	print 'no file need to replace,finish...'


print '==============start load replace file list =============='
normalConfigFilePathList = configFileDic['normalConfigFilePathList']
frameworkResHwextConfigFilePathList = configFileDic['frameworkResHwextConfigFilePathList']
print '==============start load replace file list =============='

print '==============start replace=============='
print '==============first ,replace frameworkResHwextConfigFilePathList============== '  
for item in frameworkResHwextConfigFilePathList:
	doTransform(item , framework_res_hwext_change_v91_v10)
print '==============then ,replace  frameworkResHwextConfigFilePathList============== '  

print '==============then , replace normalConfigFilePathList============== '  
for item in normalConfigFilePathList:
	print item
	# print item.split('/')[len(item.split('/')) - 2 ].split('.')[len(item.split('/')[len(item.split('/')) - 2 ].split('.'))-1]
	print 'item:%s , normalcnofig_dic:%s' %( item , item.split('/')[len(item.split('/')) - 2 ].split('.')[len(item.split('/')[len(item.split('/')) - 2 ].split('.'))-1] )
	if isWindows:
		doTransform(item , normalConfig_dic['%s_normalConfig_v91_v10' %( item.split('\\')[len(item.split('\\')) - 2 ].split('.')[len(item.split('\\')[len(item.split('\\')) - 2 ].split('.'))-1]  )] )
	else:
		doTransform(item , normalConfig_dic['%s_normalConfig_v91_v10' %( item.split('/')[len(item.split('/')) - 2 ].split('.')[len(item.split('/')[len(item.split('/')) - 2 ].split('.'))-1]  )] )
print '==============then ,replace normalConfigFilePathList============== '  

print '==============checkIcons============== '  
checkIcons()
print '==============checkIcons============== '  

print '==============checkdot9pic============== '  
# checkdot9pic()
print '==============checkdot9pic============== '  


print '==============updateLauncher============== '  
updateLauncher()
print '==============updateLauncher============== '  


print '==============udpateSystemUi============== '  
udpateSystemUi()
print '==============udpateSystemUi============== '  


print '==============updateThemeDesc============== '  
updateThemeDesc()
print '==============updateThemeDesc============== '  


# 完成
print '==============finish replace  ,now print the losted pic or icons list （icons, dot9pic）============== ' 
for item in queshipicArr :
	print item

