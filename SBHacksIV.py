from flask import Flask, render_template
import io
import os
import google.cloud.vision

app = Flask(__name__)

vision_client = google.cloud.vision.ImageAnnotatorClient()
test_image = './test.jpg'

with io.open(test_image, 'rb') as image_file:
    content = image_file.read()

image = google.cloud.vision.types.Image(content=content)
response = vision_client.document_text_detection(image=image)
doc = response.full_text_annotation

for page in doc.pages:
    for block in page.blocks:
        block_words = []
        for paragraph in block.paragraphs:
            #block_words.extend(paragraph.words)
            block_words = paragraph.words
            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)
            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text
        #
        # block_symbols = []
        # for word in block_words:
        #     block_symbols.extend(word.symbols)
        #
        # block_text = ''
        # for symbol in block_symbols:
        #     block_text = block_text + symbol.text

        print('Block Content: {}'.format(block_text))
        #print('Block Bounds:\n {}'.format(block.bounding_box))

# print('Texts:')
#
# for text in texts:
#     print(text)
#
#     # print('\n"{}"'.format(text.description))
#     #
#     # verticies = (['({},{})'.format(vertex.x, vertex.y)
#     #               for vertex in text.bounding_poly.vertices])
#     # print('bounds: {}'.format('.'.join(verticies)))

@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
