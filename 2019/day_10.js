import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { manhattan, Point } from '../js_utils/utils.js';

console.time('run');
let data = parseInput();
let {newStation, detected} = findMaxDetected();
switch (argv[2]) {
	case '1':
		console.log(Object.keys(detected).length)
		break
	case '2':
		const point = vaporize();
		console.log(100 * point.x + point.y);
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
	let res = [];
	for (const [y, line] of raw.split('\n').entries()) {
		for (const [x, char] of line.split('').entries()) {
			if (char === '#') {
				res.push(new Point(x, y));
			}
		}
	}
	return res
}

function findSlope(p1, p2) {
	// Only slope of line is relevant here
	// First number is used to track both sides of the line
	if (p1.x === p2.x) {
		return JSON.stringify([p1.y < p2.y ? 1 : -1, Infinity])
	}
	if (p1.y === p2.y) {
		return JSON.stringify([p1.x < p2.x ? -1 : 1, 0])
	}
	return JSON.stringify([
		p1.x < p2.x ? -1 : 1,
		(p1.y - p2.y) / (p1.x - p2.x),
	])
}

function findMaxDetected() {
	let maxDetected = 0;
	let station;
	for (const point of data) {
		let detected = {};
		for (const otherPoint of data) {
			if (point != otherPoint) {
				const params = findSlope(point, otherPoint);
				detected[params] ? detected[params].push(otherPoint) : detected[params] = [otherPoint];
			}
		}
		if (Object.keys(detected).length > Object.keys(maxDetected).length) {
			maxDetected = detected;
			station = point;
		}
	}
	return {newStation: station, detected: maxDetected}
}

function vaporize() {
	var slopes = Object.keys(detected);
	slopes.sort((x, y) => {
		let [sideX, slopeX] = JSON.parse(x);
		let [sideY, slopeY] = JSON.parse(y);
		if (slopeX === null) { 
			slopeX = sideX * Infinity;
			sideX = -1;
		}
		if (slopeY === null) { 
			slopeY = sideY * Infinity;
			sideY = -1;
		}
		if (sideX < sideY) {
			return -1
		}
		if (sideX === sideY && slopeX < slopeY) {
			return -1
		}
		if (sideX === sideY && slopeX > slopeY) {
			return 1
		}
		return 1
	})
	return detected[slopes[199]].sort((x, y) => {
		if (manhattan(newStation, x) < manhattan(newStation, y)) {
			return -1
		}
		// no equality possible here
		return 1
	})[0]
}