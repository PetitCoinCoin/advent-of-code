import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { isLower } from '../js_utils/utils.js';

console.time('run');
let data = {};
const start = parseInput();
let compressedData = {};
switch (argv[2]) {
	case '1':
		console.log(collectKeys(start, compressTunnel(start)));
		break
	case '2':
		const starts = updateTunnel();
		console.log(
			starts
			.map(s => collectKeys(s, compressTunnel(s)))
			.reduce((tot, acc) => tot + acc, 0)
		);
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
	let position;
	for (const [y, line] of raw.split('\n').entries()) {
		for (const [x, char] of line.split('').entries()) {
			if (char !== '#' && char !== '') {
				data[[x, y]] = char;
				if (char === '@') {
					position = [x, y];
					data[[x, y]] = '.';
				}
			}
		}
	}
	return position
}

function compressTunnel(s) {
	let keys = new Set();
	let mainQueue = [s];
	let mainSeen = {};
	while (mainQueue.length > 0) {
		const init = mainQueue.shift();
		if (mainSeen[init] !== undefined) {
			continue
		}
		mainSeen[init] = true;
		let queue = [[0, init[0], init[1], '']];
		let seen = {};
		while (queue.length > 0) {
			let [dist, x, y, doors] = queue.shift();
			if (seen[[x, y]] !== undefined) {
				continue
			}
			seen[[x, y]] = true;
			for (const [dx, dy] of [[0, 1], [0, -1], [1, 0], [-1, 0]]) {
				const char = data[[x + dx, y + dy]] ;
				if (char === undefined || (x + dx === init[0] && y + dy === init[1])) {
					continue
				}
				if (seen[[x + dx, y + dy]] !== undefined) {
					continue
				}
				if (char=== '.') {	
					queue.push([dist + 1, x + dx, y + dy, doors]);
				} else {
					if (isLower(char)) {
						keys.add(char);
						if (compressedData[init] === undefined) {
							compressedData[init] = {};
						}
						if (compressedData[[x + dx, y + dy]] === undefined) {
							// console.log('là')
							compressedData[[x + dx, y + dy]] = {};
						}
						compressedData[init][[x + dx, y + dy]] = [dist + 1, doors.toLowerCase()];
						if (init[0] !== s[0] && init[1] !== s[1]) {
							compressedData[[x + dx, y + dy]][init] = [dist + 1, doors.toLowerCase()];
						}
						mainQueue.push([x + dx, y + dy]);
					}
					queue.push([dist + 1, x + dx, y + dy, isLower(char) ? doors : doors + char]);
				}
			}
		}
	}
	return keys
}

function collectKeys(s, kCount) {
	let queue = [[0, String(s), '']];
	let seen = {};
	while (queue.length > 0) {
		queue.sort((a1, a2) => {
			if (a1[0] < a2[0]) {
				return -1
			}
			if (a1[0] > a2[0]) {
				return 1
			}
			// same distance
			if (a1[2].length > a2[2].length) {
				return -1
			}
			if (a1[2].length < a2[2].length)  {
				return 1
			}
			return 0
		})
		let [dist, pos, keys] = queue.shift();
		if (keys.length === kCount.size) {
			return dist
		}
		if (seen[pos + keys] !== undefined) {
			continue
		}
		seen[pos + keys] = true;
		for (const [coord, item] of Object.entries(compressedData[pos])) {
			const [d, doors] = item;
			const char = data[coord];
			if (keys.includes(char)) {
				continue
			}
			if ([...doors].some(val => kCount.has(val) && !keys.includes(val))) {
				continue
			}
			queue.push([dist + d, coord, keys.includes(char) ? keys : [...(keys + char)].sort().join('')]);
		}
	}
	return 0
}

function updateTunnel() {
	[[0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]].forEach(([dx, dy]) => delete data[[start[0] + dx, start[1] + dy]])
	return [[1, 1], [1, -1], [-1, -1], [-1, 1]].map(([dx, dy]) => [start[0] + dx, start[1] + dy])
}
