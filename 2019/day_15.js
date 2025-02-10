import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
const directionMap = {
	1: [0, 1],
	2: [0, -1],
	3: [-1, 0],
	4: [1, 0],
}
let oxygen;
let relativeBase = 0;
let inputs = [1, 2, 3, 4];
let output = 0;
move(argv[2] === '1');
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

function run(i, arr, input) {
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
			arr[arr[i + 1] + (p1 == 2 ? relativeBase : 0)] = input;
			return {isDone: false, step: 2}
		case 4:
			output = param1;
			return {isDone: true, step: 2}
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

function intCode(start, arr, input) {
	let i = start;
	while (i<arr.length) {
		const {isDone, step} = run(i, arr, input)
		if (isDone) {
			return [i + step, arr]
		}
		i += step
	}
}

function move(isPartOne) {
	let seen = {};
	let grid = {};
	let isDone = false;
	let queue = [[0, 0, 0, 1, data]];
	while (queue.length > 0) {
		let [start, x, y, step, program] = queue.shift();
		if (seen[[x, y]] !== undefined) {
			continue
		}
		seen[[x, y]] = true;
		for (const inp of inputs) {
			const [dx, dy] = directionMap[inp];
			if (seen[[x + dx, y + dy]] !== undefined) {
				continue
			}
			let [nextStart, nextProgram] = intCode(start, [...program], inp);
			if (output == 2) {
				if (isPartOne) {
					isDone = true;
					console.log(step)
					break
				} else {
					oxygen = [x + dx, y + dy];
					grid[[x + dx, y + dy]] = true;
				}
			} else if (output == 1) {
				queue.push([nextStart, x + dx, y + dy, step + 1, nextProgram])
				grid[[x + dx, y + dy]] = true;
			} 
		}
		if (isDone) {
			break
		}
	}
	if (!isPartOne) {
		console.log(reverseMove(grid));
	}
}

function reverseMove(grid) {
	let queue = [oxygen];
	let seen = {};
	let duration = -1;
	while (queue.length > 0) {
		let newQueue = [];
		while (queue.length > 0) {
			const [x, y] = queue.pop();
			seen[[x, y]] = true;
			for (const [dx, dy] of Object.values(directionMap)) {
				if (grid[[x + dx, y + dy]] === true && seen[[x + dx, y + dy]] === undefined) {
					newQueue.push([x + dx, y + dy]);
				}
			}
		}
		queue = [...newQueue];
		duration += 1;
	}
	return duration
}
