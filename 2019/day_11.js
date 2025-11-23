import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { range, Point } from '../js_utils/utils.js';

console.time('run');
let data = parseInput();
let panels = {};
let position = new Point(0, 0);
// 0 is up, direction is represented mod 4, add 1 to turn right
let direction = 0;
let relativeBase = 0;
let outputs = 0;
switch (argv[2]) {
	case '1':
		intCode();
		console.log(Object.keys(panels).length);
		break
	case '2':
		panels[JSON.stringify(position)] = 1;
		intCode();
		pprint();
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
			data[data[i + 1] + (p1 == 2 ? relativeBase : 0)] = panels[JSON.stringify(position)] || 0;
			return {isDone: false, step: 2}
		case 4:
			outputs += 1;
			outputs % 2 === 1 ? paint(param1) : move(param1);
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

function paint(color) {
	panels[JSON.stringify(position)] = color;
	return
}

function move(dir) {
	direction = (4 + direction + (dir === 1 ? 1 : -1)) % 4;
	switch (direction) {
		case 0:
			position.y += 1
			break;
		case 1:
			position.x += 1
			break;
		case 2:
			position.y -= 1;
			break;
		case 3:
			position.x -= 1;
			break;
		default:
			throw 'wtf'
	}
}

function pprint() {
	let minX = Infinity;
	let minY = Infinity;
	let maxX = 0;
	let maxY = 0;
	for (const pos of Object.keys(panels)) {
		const {x, y} = JSON.parse(pos);
		minX = Math.min(minX, x);
		minY = Math.min(minY, y);
		maxX = Math.max(maxX, x);
		maxY = Math.max(maxY, y);
	}
	for (const y of range(maxY + 1, minY - 2, -1)) {
		console.log(range(minX - 1, maxX + 2).map(x => {
			return (panels[JSON.stringify(new Point(x, y))] || 0) === 0 ? ' ' : '#' 
		}).join(''));
	}
}
