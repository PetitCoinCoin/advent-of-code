import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { range } from '../js_utils/utils.js';

console.time('run');
let data = parseInput();
let relativeBase = 0;
let grid = {};
let x = 0;
let y = 0;
let shouldPrint = false;
// For part 2, I just pretty printed the map and found path and patterns manually.
const inputs = [...(([
	'A,B,A,B,A,C,B,C,A,C',
	'R,4,L,10,L,10',
	'L,8,R,12,R,10,R,4',
	'L,8,L,8,R,10,R,4',
	'n\n',
].join('\n')))].map(char => char.codePointAt(0));
switch (argv[2]) {
	case '1':
		intCode();
		console.log(findIntersections().map(a => a[0] * a[1]).reduce((tot, acc) => tot + acc, 0));
		pprint();
		break
	case '2':
		shouldPrint = true;
		data[0] = 2;
		intCode();
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
	return raw.split(',').map(Number)
}

function getModes(value) {
	return {
		opcode: value % 100,
		p1: Math.floor((value % 1000) / 100),
		p2: Math.floor((value % 10000) / 1000),
		p3: Math.floor(value / 10000),  // value is not supposed to be on 6 digits
	}
}

function run(i) {
	const {opcode, p1, p2, p3} = getModes(data[i]);
	const relativ1 = (p1 == 2 ? data[data[i + 1] + relativeBase] : data[data[i + 1]]) || 0;
	const relativ2 = (p2 == 2 ? data[data[i + 2] + relativeBase] : data[data[i + 2]]) || 0;
	const param1 = p1 == 1 ? data[i + 1] : relativ1;
	const param2 = p2 == 1 ? data[i + 2] : relativ2;
	const param3 = (p3 == 2 ? data[i + 3] + relativeBase : data[i + 3]) || 0;  // should never be in immediate mode
	switch (opcode) {
		case 1:
			data[param3] = param1 + param2;
			return {isDone: false, step: 4}
		case 2:
			data[param3] = param1 * param2;
			return {isDone: false, step: 4}
		case 3:
			data[data[i + 1] + (p1 == 2 ? relativeBase : 0)] = inputs.shift();
			return {isDone: false, step: 2}
		case 4:
			if (shouldPrint) {
				console.log(param1)
			}
			const char = String.fromCharCode(param1);
			if (char === '\n') {
				y += 1;
				x = 0;
			} else {
				grid[[x, y]] = char;
				x += 1;
			}
			return {isDone: false, step: 2}
		case 5:
			var step = param1 != 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 6:
			var step = param1 == 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 7:
			data[param3] = param1 < param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 8:
			data[param3] = param1 == param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 9:
			relativeBase += param1;
			return {isDone: false, step: 2}
		case 99:
			return {isDone: true, step: 0}
		default:
			throw 'wtf'
	}

}

function intCode() {
	let i = 0;
	while (i<data.length) {
		const {isDone, step} = run(i)
		if (isDone) {
			return
		}
		i += step
	}
}

function findIntersections() {
	var intersect = [];
	for (const [pos, char] of Object.entries(grid)) {
		if (char === '.' || char === 'X') {
			continue
		}
		const [rx, ry] = pos.split(',').map(Number);
		if (
			grid[[rx + 1, ry]] === '#'
			&& grid[[rx - 1, ry]] === '#'
			&& grid[[rx, ry + 1]] === '#'
			&& grid[[rx, ry - 1]] === '#'
		) {
			intersect.push([rx, ry]);
		}
	}
	return intersect
}


function pprint() {
	let minX = Infinity;
	let minY = Infinity;
	let maxX = 0;
	let maxY = 0;
	for (const pos of Object.keys(grid)) {
		const [x, y] = pos.split(',').map(Number);
		minX = Math.min(minX, x);
		minY = Math.min(minY, y);
		maxX = Math.max(maxX, x);
		maxY = Math.max(maxY, y);
	}
	for (const y of range(minY - 1, maxY + 2)) {
		console.log(range(minX - 1, maxX + 2).map(x => grid[[x, y]]).join('') + y);
	}
}
