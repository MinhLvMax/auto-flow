from src.chatbot.llm import scan_directory, build_tree, save_json

path = r'C:\Users\Admin\Downloads\Script_Editor_App (code)\Script_Editor_App'
# tree = scan_directory(path)
tree = build_tree(path)
# from pprint import pprint
# pprint(tree)
save_json(tree, 'tree.json')