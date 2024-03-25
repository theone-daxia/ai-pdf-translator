import sys
import os
from gooey import Gooey

# 添加当前脚本所在目录到 Python 解释器的搜索路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import GuiArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator


# 使用 gooey 将命令行转为 gui
@Gooey(program_name='AI-PDF-Translator', encoding='utf-8', language='chinese')
def main():
    argument_parser = GuiArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)

    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']
    # 支持翻译成指定语言
    target_language = args.target_language if args.target_language else config['common']['target_language']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format, target_language)


if __name__ == "__main__":
    main()
