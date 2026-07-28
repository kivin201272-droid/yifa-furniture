const Tesseract = require('tesseract.js');
const path = require('path');

const bedroomImages = [
    'img-008.jpg', 'img-011.jpg', 'img-015.jpg', 'img-019.jpg',
    'img-025.jpg', 'img-031.jpg', 'img-036.jpg', 'img-041.jpg',
    'img-050.jpg', 'img-056.jpg', 'img-063.jpg', 'img-072.jpg',
    'img-080.jpg', 'img-085.jpg'
];

async function run() {
    for (const img of bedroomImages) {
        const imgPath = path.join(__dirname, 'assets/images/pdf3', img);
        console.log(`Processing ${img}...`);
        try {
            const { data: { text } } = await Tesseract.recognize(imgPath, 'eng');
            console.log(`[${img}] -> ${text.replace(/\n/g, ' ')}`);
        } catch (e) {
            console.error(`Error on ${img}:`, e.message);
        }
    }
}
run();
