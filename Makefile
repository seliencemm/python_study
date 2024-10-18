SHELL=/bin/bash

.PHONY: aigc moderation asa aigc_foreign_teacher aigc_summarize

########################################
############# AIGC 集成测试 #############
########################################
# make aigc env=qa
aigc:
	hurl --very-verbose --test --variables-file aigc/env/$(env).env --max-time 15 aigc/*.hurl

aigc_foreign_teacher:
	rm -rf aigc/report/*   # 清空报告
	hurl --very-verbose --continue-on-error --test --report-html aigc/report/ --variables-file aigc/env/$(env).env --max-time 30 aigc/foreign_teacher/

aigc_summarize:
	hurl --very-verbose --test --variables-file aigc/env/$(env).env --max-time 15 aigc/summarize.hurl

###################################################
############# Live Translator 集成测试 #############
###################################################
# make live_translator env=qa
live_translator:
	mkdir -p live_translator/report/
	hurl --very-verbose --continue-on-error --test --report-html live_translator/report/ --variables-file live_translator/env/$(env).env --max-time 60 live_translator/translate/text_translate/*.hurl

live_translator_moderation:
	hurl --very-verbose --test --variables-file live_translator/env/$(env).env --max-time 15 live_translator/moderation.hurl

live_translator_asa:
	hurl --very-verbose --test --variables-file live_translator/env/$(env).env --max-time 15 live_translator/asa.hurl

live_translator_translate:
	hurl --very-verbose --continue-on-error --test --variables-file live_translator/env/uat.env --max-time 60 live_translator/translate/text_translate/*.hurl
