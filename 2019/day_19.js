import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { range } from '../js_utils/utils.js';

console.time('run');
let data = parseInput();
let relativeBase = 0;
let inputs;
let pulled = 0;
let grid = {};
let px, py;
switch (argv[2]) {
	case '1':
		for (const x of range(0, 50)) {
			for (const y of range(0, 50)) {
				inputs = [x, y];
				px = x;
				py = y;
				intCode([...data]);
			}
		}
		pprint();  // Visualisation for part 2
		console.log(pulled);
		break
	case '2':
		const yMax = 5000;
		let xLeft, xRight;
		let x = yMax;
		while (xRight === undefined) {
			inputs = [x, yMax];
			px = x;
			py = yMax;
			intCode([...data]);
			if (xLeft === undefined && grid[[px, py]] === '#') {
				xLeft = x;
			}
			if (xLeft !== undefined && grid[[px, py]] === '.') {
				xRight = x - 1;
			}
			x++;
		}
		const xStart = 4;
		const yStart = 3;
		const slopeBelow = (yMax - yStart) / (xLeft - xStart);
		const slopeAbove = (yMax - yStart) / (xRight - xStart);
		let y = 100;
		let delta = Infinity;
		while (delta >= 0.5) {
			y++;
			const xAbove = (y - yStart) / slopeAbove + xStart;
			const xBelow = (y + 99 - yStart) / slopeBelow + xStart;
			delta = Math.abs(xAbove - 99 - xBelow);
		}
		console.log(y + 10000 * Math.round((y + 99 - yStart) / slopeBelow + xStart))
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

function run(i, arr) {
	const {opcode, p1, p2, p3} = getModes(arr[i]);
	const relativ1 = (p1 == 2 ? arr[arr[i + 1] + relativeBase] : arr[arr[i + 1]]) || 0;
	const relativ2 = (p2 == 2 ? arr[arr[i + 2] + relativeBase] : arr[arr[i + 2]]) || 0;
	const param1 = p1 == 1 ? arr[i + 1] : relativ1;
	const param2 = p2 == 1 ? arr[i + 2] : relativ2;
	const param3 = (p3 == 2 ? arr[i + 3] + relativeBase : arr[i + 3]) || 0;  // should never be in immediate mode
	switch (opcode) {
		case 1:
			arr[param3] = param1 + param2;
			return {isDone: false, step: 4}
		case 2:
			arr[param3] = param1 * param2;
			return {isDone: false, step: 4}
		case 3:
			arr[arr[i + 1] + (p1 == 2 ? relativeBase : 0)] = inputs.shift();
			return {isDone: false, step: 2}
		case 4:
			pulled += param1;
			grid[[px, py]] = param1 === 1 ? '#' : '.';  // only for visualisation
			return {isDone: false, step: 2}
		case 5:
			var step = param1 != 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 6:
			var step = param1 == 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 7:
			arr[param3] = param1 < param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 8:
			arr[param3] = param1 == param2 ? 1 : 0;
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

function intCode(arr) {
	let i = 0;
	while (i<arr.length) {
		const {isDone, step} = run(i, arr)
		if (isDone) {
			return
		}
		i += step
	}
}

function pprint() {
	for (const y of range(0, 50)) {
		console.log(range(0, 50).map(x => grid[[x, y]]).join('') + y);
	}
}
