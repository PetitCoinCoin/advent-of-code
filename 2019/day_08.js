import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
const width = 25;
const height = 6;
const image = buildImage();
switch (argv[2]) {
	case '1':
		console.log(checkSum());
		break
	case '2':
		renderImage();
		break
	default:
		throw 'Please set a part to solve (1 or 2)';
}
console.timeEnd('run');

function readInput() {
	const inputFilename = `inputs/${basename(import.meta.url, '.js')}.txt`;
	return fs
		.readFileSync(inputFilename)
		.toString()
		.trim()
}

function parseInput() {
	let raw = readInput();
	return raw.split('').map(Number)
}

function buildImage() {
	var result = {};
	var layer = 0;
	var start = 0;
	while (start < data.length) {
		result[layer] = data.slice(start, start + width * height);
		start += width * height;
		layer++;
	};
	return result
}

function checkSum() {
	let min_layer = 0;
	let min_zero = Infinity;
	for (const [layer, pixels] of Object.entries(image)) {
		const count_zero = pixels.filter(x => x == 0).length;
		if (count_zero < min_zero) {
			min_zero = count_zero;
			min_layer = layer;
		}
	}
	return image[min_layer].filter(x => x === 1).length * image[min_layer].filter(x => x === 2).length
}

function renderImage() {
	var rendered = Array(width * height).fill(undefined);
	var layer = 0;
	while (rendered.some(x => x === undefined) && layer < (data.length / (width * height))) {
		for (const [i, value] of image[layer].entries()) {
			if (rendered[i] === undefined && value !== 2) {
				rendered[i] = value;
			}
		}
		layer++;
	}
	var start = 0;
	while (start < rendered.length) {
		console.log(rendered.slice(start, start + width).map(x => x === 1 ? '#' : ' ').join(''));
		start += width;
	}
}
