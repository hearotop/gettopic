from bs4 import BeautifulSoup
import os
import time

# 读取 HTML 文件
def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 创建资源文件夹
def create_resource_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# 处理题目类型块
def process_question_type_blocks(soup):
    output_content = ''
    question_type_blocks = soup.find_all('div', class_=['mark_item ans-cc', 'mark_item'])
    for block in question_type_blocks:
        question_type = block.find('h2', class_='type_tit').get_text(strip=True)
        output_content += f'{question_type}\n\n'
        questions = block.find_all(['h3', 'div'], class_=['mark_name colorDeep', 'essay_question'])
        if questions:
            question_number = 1
            for question in questions:
                output_content += f'{question_number}. '
                question_number += 1
                if question.name == 'h3':
                    question_text_elem = question.find('span', class_='qtContent')
                    question_text = question_text_elem.get_text(strip=True) if question_text_elem else "无题目内容"
                elif question_type == '简答题':
                    question_elements = [span for element in soup.find_all('span', class_='qtContent') for span in element.find_all('span')]
                    answer_elements = soup.find_all('dd', class_='rightAnswerContent')
                    if question_elements and answer_elements:
                        for i, (q, a) in enumerate(zip(question_elements, answer_elements), start=1):
                            question_text = q.get_text(strip=True)
                            output_content += f'{question_text}\n'
                            answer_text = ''.join([p.get_text(strip=True) for p in a.find_all('p')]).strip()
                            output_content += f'{answer_text}\n\n'
                    else:
                        output_content += "简答题无题目或答案\n\n"
                else:
                    question_text = "无题目内容"
                output_content += f'{question_text}\n'
                images = question.find_all('img')
                for img in images:
                    img_url = img.get('src')
                    if img_url:
                        output_content += f'![{img_url}]({img_url})\n'
                question_details = question.find_next_sibling('ul', class_='mark_letter colorDeep qtDetail')
                if question_details:
                    for detail in question_details.find_all('li'):
                        output_content += f'{detail.get_text(strip=True)}\n'
                        detail_images = detail.find_all('img')
                        for img in detail_images:
                            img_url = img.get('src')
                            if img_url:
                                output_content += f'![{img_url}]({img_url})\n'
                if question_type != '简答题':
                    correct_answer_block = question.find_next('div', class_='mark_answer')
                    if correct_answer_block:
                        correct_answer_elem = correct_answer_block.find('span', class_='rightAnswerContent') or correct_answer_block.find('dd', class_='rightAnswerContent')
                        if correct_answer_elem:
                            correct_answer = correct_answer_elem.get_text(strip=True)
                            output_content += f'正确答案: {correct_answer}'
                        else:
                            output_content += "无正确答案"
                        answer_images = correct_answer_block.find_all('img')
                        for img in answer_images:
                            img_url = img.get('src')
                            if img_url:
                                output_content += f'![{img_url}]({img_url})'
                    else:
                        output_content += "无正确答案块"
                output_content += '\n\n'
        else:
            output_content += f'{question_type} 无题目\n\n'
    return output_content

# 写入 Markdown 文件
def write_to_markdown(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == '__main__':
    html_file_path = 'd:/markdown/test.html'
    html_content = read_html_file(html_file_path)
    soup = BeautifulSoup(html_content, 'html.parser')
    resource_folder = 'd:/markdown/resource'
    create_resource_folder(resource_folder)
    output_content = process_question_type_blocks(soup)
    timestamp = time.strftime('%Y-%m-%d_%H%M%S')
    tip_file_path = f'tip_{timestamp}.md'
    write_to_markdown(tip_file_path, output_content)

