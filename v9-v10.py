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

isWindows = False

queshipicArr = []

currentProjectFilePath = ''

fileList = ['com.android.contacts' , 'com.android.mms'  ,'com.android.phone' , 'com.android.phone.recorder' , 'com.android.server.telecom' , 'com.android.systemui' ,
	'com.huawei.android.launcher' , 'com.huawei.hwvoipservice'
]


framework_res_hwext_change_v9_v10=[
	{
		'orgin':'<color name="hwtoolbar_background">(.*)</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_appbar_bg_blur">{color}</color>','color':'{orgincolor}00'}]
	},
	{
		'orgin':'<color name="hwtoolbar_background">(.*)</color>',
		'replace':[{'tag':'<color name="emui_toolbar_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_toolbar_bg_blur">{color}</color>','color':'{orgincolor}00'}]
	},
	{
		'orgin':'<color name="navigationbar_emui_light">(.*)</color>',
		'replace':[{'tag':'<color name="emui_navigationbar_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_navigationbar_bg_blur">{color}</color>','color':'{orgincolor}00'}]
	},
	{
		'orgin':'<color name="emui_color_gray_1">(.*)</color>',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>','color':'{orgincolor}FF'},{'tag':'<color(.*)name="emui_subtab_bg_blur">{color}</color>','color':'{orgincolor}00'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_tips_bg">{color}</color>','color':'#F2D9D9D9'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'#FFFFFFFF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_control_normal">{color}</color>','color':'#19000000'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_toast_bg">{color}</color>','color':'#F2D9D9D9'}]
	},
]
framework_res_hwext_change_v91_v10=[
	# 默认颜色则直接修改  非默认颜色保持不变

	# 颜色必须保持一致开始 
	{
		'orgin':'<color name="emui_appbar_bg">#F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>','color':'#E6FFFFFF'}]
	},
	{
		'orgin':'<color name="emui_appbar_bg_blur">#80F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg_blur">{color}</color>','color':'#FF000000'}]
	},
	{
		'orgin':'<color name="emui_toolbar_bg">#FF262626</color>',
		'replace':[{'tag':'<color name="emui_toolbar_bg">{color}</color>','color':'#F2FAFAFA'}]
	},
	{
		'orgin':'<color name="emui_toolbar_bg_blur">#80262626</color>',
		'replace':[{'tag':'<color name="emui_toolbar_bg">{color}</color>','color':'#F2FAFAFA'}]
	},
	{
		'orgin':'<color name="emui_appbar_bg">#F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg">{color}</color>','color':'#E6FFFFFF'}]
	},
	{
		'orgin':'<color name="emui_appbar_bg_blur">#80F2F2F2</color>',
		'replace':[{'tag':'<color name="emui_appbar_bg_blur">{color}</color>','color':'#FF000000'}]
	},
	{
		'orgin':'<color name="emui_navigationbar_bg">#FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_navigationbar_bg">{color}</color>','color':'#F2FFFFFF'}]
	},
	{
		'orgin':'<color name="emui_navigationbar_bg_blur">#80FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_navigationbar_bg_blur">{color}</color>','color':'#ff000000'}]
	},
	{
		'orgin':'<color name="emui_subtab_bg">#f0f0f0</color>',
		'replace':[{'tag':'<color name="emui_subtab_bg">{color}</color>','color':'#E6FFFFFF'}]
	},
	{
		'orgin':'<color name="emui_subtab_bg_blur">#80f0f0f0</color>',
		'replace':[{'tag':'<color name="emui_subtab_bg_blur">{color}</color>','color':'#ff000000'}]
	},
	# 颜色必须保持一致   结束

	{
		'orgin':'<color name="emui_color_tips_bg">#FF666666</color>',
		'replace':[{'tag':'<color name="emui_color_tips_bg">{color}</color>','color':'#F2D9D9D9'}]
	},
	{
		'orgin':'<color name="emui_color_bg">#ffffff</color>',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'#FFFFFFFF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_control_normal">{color}</color>','color':'#19000000'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_toast_bg">{color}</color>','color':'#F2D9D9D9'}]
	},
	{
		'orgin':'<color name="emui_color_divider_horizontal">#33FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_color_divider_horizontal">{color}</color>','color':'#33000000'}]
	},

	# 切换至.9图
	{
		'orgin':'<color name="emui_color_gray_4">#cacaca</color>',
		'replace':[{'tag':'','color':''}]
	},

	{
		'orgin':'<color name="emui_color_fg">#000000</color>',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'#FFFFFFFF'}]
	},
	
	{
		'orgin':'<color name="emui_color_fg">(.*)</color>',
		'replace':[{'tag':'<color name="emui_color_bg">{color}</color>','color':'{orgincolor}'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_connected">{color}</color>','color':'#41ba41'}]
	},
	{
		'orgin':'<color name="emui_accent">#007dfe</color>',
		'replace':[{'tag':'<color name="emui_accent">{color}</color>','color':'#FF007DFF'}]
	},
	{
		'orgin':'<color name="emui_functional_blue">#005bba</color>',
		'replace':[{'tag':'<color name="emui_functional_blue">{color}</color>','color':'#007DFF'}]
	},
	{
		'orgin':'<color name="emui_switch_bg_on">#007dfe</color>',
		'replace':[{'tag':'<color name="emui_switch_bg_on">{color}</color>','color':'#007DFF'}]
	},
	{
		'orgin':'<color name="emui_progress">#808080</color>',
		'replace':[{'tag':'<color name="emui_progress">{color}</color>','color':'#4D4D4D'}]
	},
	{
		'orgin':'<color name="emui_control_hightlight">(.*)</color>',
		'replace':[{'tag':'<color name="emui_functional_blue">{color}</color>','color':'{orgincolor}'}]
	},
	{
		'orgin':'<color name="emui_spinner_icon">(.*)</color>',
		'replace':[{'tag':'<color name="emui_color_spinner_icon">{color}</color>','color':'{orgincolor}'}]
	},
	{
		'orgin':'<color name="emui_appbar_icon">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_appbar_icon">{color}</color>','color':'#E6000000'}]
	},
	{
		'orgin':'<color name="emui_appbar_icon_pressed">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_appbar_icon_pressed">{color}</color>','color':'#E6000000'}]
	},
	{
		'orgin':'<color name="emui_appbar_title">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_appbar_title">{color}</color>','color':'#E6000000'}]
	},
	{
		'orgin':'<color name="emui_toolbar_icon">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_icon">{color}</color>','color':'#E6000000'}]
	},
	{
		'orgin':'<color name="emui_toolbar_icon_pressed">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_icon_pressed">{color}</color>','color':'#E6000000'}]
	},
	{
		'orgin':'<color name="emui_toolbar_text">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_text">{color}</color>','color':'#E6000000'}]
	},
	{
		'orgin':'<color name="emui_toolbar_text_pressed">#FF191919</color>',
		'replace':[{'tag':'<color name="emui_toolbar_text_pressed">{color}</color>','color':'#E6000000'}]
	},
	{
		'orgin':'<color name="emui_subtab_text_off">(.*)</color>',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_off">{color}</color>','color':'{orgincolor}'}]
	},
	{
		'orgin':'<color name="emui_subtab_text_off">(.*)</color>',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_off">{color}</color>','color':'{orgincolor}'}]
	},
	{
		'orgin':'<color name="emui_bottombar_icon_off">#FFFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_bottombar_icon_off">{color}</color>','color':'#99000000'}]
	},
	{
		'orgin':'<color name="emui_bottombar_text_off">#FFFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_bottombar_text_off">{color}</color>','color':'#99000000'}]
	},

	# emui_black_color_alpha_30 已删除 ，切换至.9图
	{
		'orgin':'<color name="emui_text_hint">#191919</color>',
		'replace':[{'tag':'','color':''}]
	},
	{
		'orgin':'<color name="emui_bottombar_text_off">#FFFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_bottombar_text_off">{color}</color>','color':'#99000000'}]
	},
	{
		'orgin':'<color name="emui_icon_tertiary">#191919</color>',
		'replace':[{'tag':'<color name="emui_icon_tertiary">{color}</color>','color':'#4D000000'}]
	},
	{
		'orgin':'<color name="emui_secondary">(.*)</color>',
		'replace':[{'tag':'<color name="emui_primary">{color}</color>','color':'{orgincolor}'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_appbar_subtitle">{color}</color>','color':'#99000000'}]
	},
	{
		'orgin':'<color name="emui_accent">#007dfe</color>',
		'replace':[{'tag':'<color name="emui_accent">{color}</color>','color':'#007dff'}]
	},
	{
		'orgin':'<color name="emui_fastscroll_lable_bg">#e4e4e4</color>',
		'replace':[{'tag':'<color name="emui_fastscroll_lable_bg">{color}</color>','color':'#E6E6E6'}]
	},
	{
		'orgin':'<color name="switch_off_disable_emui">#4De4e4e4</color>',
		'replace':[{'tag':'<color name="switch_off_disable_emui">{color}</color>','color':'#0E000000'}]
	},
	{
		'orgin':'<color name="emui_checkbox_boxedge">#4D000000</color>',
		'replace':[{'tag':'<color name="emui_checkbox_boxedge">{color}</color>','color':'#191919'}]
	},
	{
		'orgin':'<color name="emui_switch_outline_off">#4DFFFFFF</color>',
		'replace':[{'tag':'<color name="emui_switch_outline_off">{color}</color>','color':'#B3B3B3'}]
	},
	{
		'orgin':'<color name="emui_switch_bg_off">#FFFFFF</color>',
		'replace':[{'tag':'<color name="emui_switch_bg_off">{color}</color>','color':'#4D000000'}]
	},
	{
		'orgin':'<color name="emui_white_bg">#e4e4e4</color>',
		'replace':[{'tag':'<color name="emui_white_bg">{color}</color>','color':'#FFFFFF'}]
	},

	# progress_primary_emui.9.png  ， progress_bg_emui.9.png   亮度调整 条  ，26*74
]

launcher_normalConfig_v91_v10 = []

contacts_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="ic_home_checkbox_off_center_color">{color}</color>' , 'color':'#FFFFFF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="ic_home_checkbox_off_rim_color">{color}</color>' , 'color':'#000000'}]
	},

	# 联系人/收藏/新建按钮背景色
	# 背景颜色：
	# <color name="hwfab_bg">#007DFF</color>
	# 背景按压颜色：
	# <color name="hwfab_pressed">#0070E5</color>
	# 图标背景投影色：
	# <color name="hwfab_shadow_start">#4D00B0FF</color>
	# <color name="hwfab_shadow_end">#4DFF00D0</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_bg">{color}</color>' , 'color':'#007DFF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_pressed">{color}</color>' , 'color':'#0070E5'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_shadow_start">{color}</color>' , 'color':'#4D00B0FF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_shadow_end">{color}</color>' , 'color':'#4DFF00D0'}]
	},

	# 拨号/拨号盘展开收起悬浮按钮背景色
	# 背景颜色：
	# nomal状态
	# <color name="dial_fab_backgrounp">#41ba41</color>
	# pressed状态
	# <color name="dial_fab_backgrounp_pressed">#41ba41</color>
	# focused状态
	# <color name="dial_fab_backgrounp_focue">#41ba41</color>
	# 图标背景投影色：
	# <color name="dial_hwfab_shadow_start">#4D00B0FF</color>
	# <color name="dial_hwfab_shadow_end">#4DFF00D0</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_fab_backgrounp">{color}</color>' , 'color':'#41ba41'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_fab_backgrounp_pressed">{color}</color>' , 'color':'#41ba41'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_fab_backgrounp_focue">{color}</color>' , 'color':'#41ba41'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_hwfab_shadow_start">{color}</color>' , 'color':'#4D00B0FF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="dial_hwfab_shadow_end">{color}</color>' , 'color':'#4DFF00D0'}]
	},

	# 拨号图标
	# 图标背景色nomal状态，引用 framework-res-hwext：
	# <color name="emui_color_connected">#41ba41</color>
	# 图标背景色pressed状态，
	# <color name="contact_svg_icon_base_green_color_a">#20A934</color>
	# 图标颜色，引用 framework-res-hwext：
	# <color name="emui_color_fg_inverse">#ffffff</color>
	# 图标不可用颜色，引用 framework-res-hwext：
	# <color name="emui_color_fg_inverse">#ffffff</color>叠加38%不透明度
	# 图标按压色：
	# <color name="contact_svg_icon_base_grey_color_c">#D6D6D6</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_connected">{color}</color>' , 'color':'#41ba41'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="contact_svg_icon_base_green_color_a">{color}</color>' , 'color':'#20A934'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_fg_inverse">{color}</color>' , 'color':'#ffffff'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="emui_color_fg_inverse">{color}</color>' , 'color':'#ffffff'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="contact_svg_icon_base_grey_color_c">{color}</color>' , 'color':'#D6D6D6'}]
	},


	{
		'orgin':'',
		'replace':[{'tag':'<color name="bottom_tab_bg">{color}</color>' , 'color':'#ffffff'}]
	},

	# 拨号/联系人、收藏主界面/新建按钮（可保留默认状态）
	# 拨号/悬浮图标颜色
	# <color name="hwfab_icon_start">#00B0FF</color>
	# <color name="hwfab_icon_end">#FF00D0</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_icon_start">{color}</color>' , 'color':'#00B0FF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwfab_icon_end">{color}</color>' , 'color':'#FF00D0'}]
	},

	# 联系人首次启动条幅背景色
	# <color name="tips_and_divider_color">#FFFFFFFF</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="tips_and_divider_color">{color}</color>' , 'color':'#FFFFFFFF'}]
	},

	# <color name="hwsubtab_emui_color_bg">#ffffff</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_emui_color_bg">{color}</color>' , 'color':'#ffffff'}]
	},

	# 选中的页签文字颜色：<color name="hwsubtab_emui_subtab_text_on">#007dff</color>
	# 下划线图标颜色：<color name="hwsubtab_indicator_color">#007dff</color>
	# 未选中的页签文字颜色：<color name="hwsubtab_emui_subtab_text_off">#191919</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_on">{color}</color>' , 'color':'#007dff'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_indicator_color">{color}</color>' , 'color':'#007dff'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hwsubtab_emui_subtab_text_off">{color}</color>' , 'color':'#191919'}]
	},

	# svg图片，即电话或者摄像头图标的颜色：<color name="hicall_recent_call_type_image">#FFFFFF</color>
	# 灰色背景颜色:  引用 framework-res-hwext：
	# <color name="emui_primary">#191919</color>叠加  38%不透明
	# 灰色背景周围白色描边颜色:  引用 framework-res-hwext：
	# <color name="emui_color_bg">#ffffff</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="hicall_recent_call_type_image">{color}</color>' , 'color':'#FFFFFF'}]
	},

	# 新增.9图
	# 图标背景资源：daier_call_btn_normal.png
	# 图标背景按压资源：daier_call_btn_press.png
	# dialpad_background_drawable.9.png 拨号键盘中间间隔 ，无固定尺寸
	# header_background4.9.png
]

# hwvoipservice 新增包 直接用官方包替代
hwvoipservice_normalConfig_v91_v10 = []

mms_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="color_gray_one">{color}</color>' , 'color':'#F2FAFAFA'}]
	},


	# 新增.9图
	# <!-- 待发区信息气泡背景颜色 -->
	# <!-- 会话界面 发送消息的泡泡的背景色 -->
	# <!-- 会话界面 接收消息的泡泡的背景颜色 -->
	# <!-- 发送加密短信发送气泡背景颜色 -->
	# <!-- 增强信息发送气泡背景颜色 -->
	# 具体
	# message_attachment_preview_bg	"172x102
	# 可以不固定，保证全区域可显示"	"待发区气泡背景
	# 如有方向，注意镜像"
	# "
	# message_location_pop_send_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 发送的地理位置气泡背景，圆角30px
	# 如有方向，注意镜像"
	# "
	# message_pop_favorite_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 收藏的发送的短信气泡背景
	# 如有方向，注意镜像"
	# "
	# message_pop_incoming_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 接收信息气泡、收藏的接收气泡背景
	# 如有方向，注意镜像"
	# "
	# message_pop_rcs_favorite_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 收藏的发送的rcs气泡背景
	# 如有方向，注意镜像"
	# "
	# message_pop_rcs_image_bg_long_press"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 四圆角蒙版气泡背景，需要有透明度，否则看不清短信文字，圆角30px
	# 如有方向，注意镜像"
	# "
	# message_pop_rcs_receive_bg_long_press"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 接收气泡蒙版气泡背景，需要有透明度，否则看不清短信文字
	# 如有方向，注意镜像"
	# "
	# message_pop_rcs_send_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# rcs发送气泡气泡背景
	# 如有方向，注意镜像"
	# "
	# message_pop_rcs_send_bg_long_press"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 发送气泡蒙版气泡背景，需要有透明度，否则看不清短信文字
	# 如有方向，注意镜像"
	# "
	# message_pop_send_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 短信发送出去之后气泡背景
	# 如有方向，注意镜像"
	# "
	# message_slide_pop_incoming_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 彩信幻灯片带图片接收气泡背景，圆角30px
	# 如有方向，注意镜像"
	# "
	# message_slide_pop_send_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 彩信幻灯片带图片发送气泡背景
	# 如有方向，注意镜像"
	# "
	# encrypted_message_pop_send_bg"	"172x102
	# 可以不固定，保证全区域可显示"	"
	# 加密短信气泡背景
	# 如有方向，注意镜像"


	# <!--增强信息 按住说话button文字颜色 -->
	# 背景引用 framework-res-hwext 切图：
	# button_big_bg_stroked.9.png（大）
	# button_small_bg_stroked.9.png（小）
	# button_big_bg_stroked_pressed.9.png（大）
	# button_small_bg_stroked_pressed.9.png（小）
	# button_big_bg_stroked_disable.9.png(大)
	# button_small_bg_stroked_disable.9.png(小)


	# 新建短信按钮颜色
	{
		'orgin':'',
		'replace':[{'tag':'<color name="mms_color_primary_dark">{color}</color>' , 'color':'#ffffff'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="messaeg_pop_text_color_send_rcs_theme_adapter">{color}</color>' , 'color':'#242424'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="message_pop_send_bg_color">{color}</color>' , 'color':'#26c73d'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="messaeg_pop_text_color_send_sms_theme_adapter">{color}</color>' , 'color':'#242424'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="messaeg_pop_text_color_send_rcs_theme_adapter">{color}</color>' , 'color':'#242424'}]
	},

	# <!-- 智能短信 弹框背景-->
	# <color name="duoqu_rcs_url_bg_color">#FFFFFF</color>
	{
		'orgin':'',
		'replace':[{'tag':'<color name="duoqu_rcs_url_bg_color">{color}</color>' , 'color':'#FFFFFF'}]
	},
]

systemui_normalConfig_v91_v10 = [
	{
		'orgin':'',
		'replace':[{'tag':'<color name="qs_customize_background_color1">{color}</color>' , 'color':'#FFFFFFFF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="notification_background_color_without_alpha">{color}</color>' , 'color':'#FFFFFFFF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="notification_button_pressed_bg_color">{color}</color>' , 'color':'#0d000000'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="notification_button_pressed_bg_color">{color}</color>' , 'color':'#0d000000'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="qs_tile_tint_on">{color}</color>' , 'color':'#FFFFFF'}]
	},

	# 背景引用 framework-res-hwext 切图：
	# button_big_bg_stroked.9.png（大）
	# button_small_bg_stroked.9.png（小）
	# button_big_bg_stroked_pressed.9.png（大）
	# button_small_bg_stroked_pressed.9.png（小）
	# button_big_bg_stroked_disable.9.png(大)
	# button_small_bg_stroked_disable.9.png(小)


	{
		'orgin':'',
		'replace':[{'tag':'<color name="volume_line_color">{color}</color>' , 'color':'#333333'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="volume_image_color">{color}</color>' , 'color':'#FF007DFF'}]
	},
	{
		'orgin':'',
		'replace':[{'tag':'<color name="volume_unfocus">{color}</color>' , 'color':'#FF007DFF'}]
	},

	# 增加.9图  ， ic_seekbar_thumb.png	96×96	音量控制滑块
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
	print '配置文件路径：' 
	print filePath
	print '修改依照配置规则：' 
	print configParam

	print '读取配置文件内容...'
	configFileContent = open(filePath).read()
	print configFileContent
	print '解析替换配置规则...'
	configFileContent = configFileContent.replace('</resources>','')
	for item in configParam:
		if item['orgin'] == '':
			print '----------'
			print '直接替换'
			for param in item['replace']:
				color = param['color'];
				replaceStr =  param['tag'].replace('{color}',color)
				print '准备添加：' + replaceStr + ',检测是否已经存在...'
				if configFileContent.find(replaceStr) > 0:
					print '存在' 
				else:
					print '不存在,准备添加'
					configFileContent+="\n\t<!-- hwv91-v10 autoadd --> \n\t" +replaceStr + "\n" 
					
			print '----------'
		else:
			print '----------'
			for param in item['replace']:
				print '计划查找' + item['orgin'] + '并替换'
				matchObj = re.search(item['orgin'] , configFileContent )
				# print matchObj
				color = ''
				replaceStr = ''
				if matchObj == None:
					print '没有发现替换项，跳过...'
					continue
				else:
					print '已找到：' + matchObj.group()
					if item['orgin'].find('(.*)') > 0 :
						color = matchObj.group(1)
						print '发现原始颜色：color:' + color
				# print '将做如下替换：' + param['tag']
				if param['tag'].find('{color}') > 0:
					color = param['color'].replace('{orgincolor}' , color)
					replaceStr = param['tag'].replace('{color}' , color)
				else:
					replaceStr = param['tag']
				print '将做如下替换：' + replaceStr
				if configFileContent.find(replaceStr) > 0:
					print '存在，不进行替换' 
				else:
					print '不存在,准备添加'
					configFileContent+="\n\t<!-- hwv91-v10 autoreplace --> \n\t" +replaceStr + "\n" 
				
			print '----------'
	configFileContent+="\n</resources>\n"
	print configFileContent
	# open(filePath , 'w').write(configFileContent)
	print '准备执行文件写入  ，文件为：' + filePath
		

def checkIcons():
	global queshipicArr
	print '检查icons.....'
	for item in icons_normalConfig_v91_v10:
		for key in item:
			print '检查对：' + key + '和' + item[key]
			filepath1 = os.path.join(currentProjectFilePath , "icons" , key + '.png')
			filepath2 = os.path.join(currentProjectFilePath , "icons" , item[key] + '.png')
			if os.path.exists(filepath1) and os.path.exists(filepath2):
				print '存在不补'
			else:
				print '不存在需补'
				print filepath1
				print filepath2
				if os.path.exists(filepath1) :
					if isWindows:
						os.system('xcopy ' + filepath1 + ' ' + filepath2)
					else:
						os.system('cp ' + filepath1 + ' ' + filepath2)
					print '已补全 ， 从' + filepath1 + '到' + filepath2
					continue
				if os.path.exists(filepath2) :
					os.system('cp ' + filepath2 + ' ' + filepath1)
					print '已补全 ， 从' + filepath2 + '到' + filepath1

					continue
				

	print '检查动态时钟图标.....'
	for item in dynamic_icons:
		if  isWindows:
			item = item.replace('/','\\',99)
		tmpPath = os.path.join(currentProjectFilePath , item ) 
		if not os.path.exists(tmpPath):	
			print '需补充:' + tmpPath
			queshipicArr.append(tmpPath)

def checkdot9pic():
	pass






# start 
# print '输入参数列表：' 
if len(sys.argv) > 1:
	for index in range(len(sys.argv)):
		if index == 1:
			currentProjectFilePath = sys.argv[index]
else:
	currentProjectFilePath = os.getcwd()
print '处理文件夹为:' + currentProjectFilePath
print '\n'
# 判断是否windows
print  '当前系统为：' + platform.system()
if platform.system().find(r'windows' ,re.I):
	isWindows = True
if isWindows:
	print 'windows环境'
else:
	print '非windows环境'

print '==============以当前文件夹为基础路径 ， 查找配置文件并替换 =============='
configFileDic = listConfigFileArray();
print '==============检查文件是否存在  ， 如果不存在 ， 则需要一个默认的组件包 ， 或移除留空=============='
configFileDic = checkFileExists(configFileDic)
print '==============检查文件是否存在  ， 如果不存在 ， 则需要一个默认的组件包 ， 或移除留空=============='

if len(configFileDic['normalConfigFilePathList']) == 0 or len(configFileDic['frameworkResHwextConfigFilePathList']) == 0:
	print '没有需要替换文件，finish...'


print '==============开始读取替换队列=============='
normalConfigFilePathList = configFileDic['normalConfigFilePathList']
frameworkResHwextConfigFilePathList = configFileDic['frameworkResHwextConfigFilePathList']
print '==============开始读取替换队列=============='

print '==============开始替换=============='
print '==============先替换 frameworkResHwextConfigFilePathList============== '  
for item in frameworkResHwextConfigFilePathList:
	doTransform(item , framework_res_hwext_change_v91_v10)
print '==============先替换 frameworkResHwextConfigFilePathList============== '  

print '==============后替换 normalConfigFilePathList============== '  
for item in normalConfigFilePathList:
	# print item
	# print item.split('/')[len(item.split('/')) - 2 ].split('.')[len(item.split('/')[len(item.split('/')) - 2 ].split('.'))-1]
	doTransform(item , normalConfig_dic['%s_normalConfig_v91_v10' %( item.split('/')[len(item.split('/')) - 2 ].split('.')[len(item.split('/')[len(item.split('/')) - 2 ].split('.'))-1]  )] )
print '==============后替换 normalConfigFilePathList============== '  

print '==============checkIcons============== '  
checkIcons()
print '==============checkIcons============== '  

print '==============checkdot9pic============== '  
checkdot9pic()
print '==============checkdot9pic============== '  


# 完成
print '==============完成替换  ，以下打印图片缺失或替换列表 （icons， .9图）============== ' 
for item in queshipicArr :
	print item
