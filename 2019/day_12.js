import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { lcmAll } from '../js_utils/utils.js';

class Moon {
	constructor(x, y, z) {
		this.x = x;
		this.y = y;
		this.z = z;
		this.vx = 0;
		this.vy = 0;
		this.vz = 0;
	}

	applyGravity(dx, dy, dz) {
		this.vx += dx;
		this.vy += dy;
		this.vz += dz;
	}

	applyVelocity() {
		this.x += this.vx;
		this.y += this.vy;
		this.z += this.vz;
	}

	potentialEnergy() {
		return Math.abs(this.x) + Math.abs(this.y) + Math.abs(this.z)
	}

	kineticEnergy() {
		return Math.abs(this.vx) + Math.abs(this.vy) + Math.abs(this.vz)
	}

	energy() {
		return this.potentialEnergy() * this.kineticEnergy()
	}
}

console.time('run');
let data = parseInput();
let repeatIndex = {'x': undefined, 'y': undefined, 'z': undefined};
switch (argv[2]) {
	case '1':
		for (var i=0; i < 1000; i++) {
			simulateStep();
		};
		console.log(data.map(m => m.energy()).reduce((acc, x) => acc + x, 0))
		break
	case '2':
		let cache = {
			'x': [],
			'y': [],
			'z': [],
		}
		var step = 0;
		while (!isDone()) {
			simulateStep();
			const separated = {
				'x': data.map(m => [m.x, m.vx]),
				'y': data.map(m => [m.y, m.vy]),
				'z': data.map(m => [m.z, m.vz]),
			}
			for (const dim of ['x', 'y', 'z'])  {
				if (repeatIndex[dim] === undefined) {
					const dimStr = JSON.stringify(separated[dim]);
					if (cache[dim].indexOf(dimStr) < 0) {
						cache[dim].push(dimStr);
					} else {
						repeatIndex[dim] = step;
					}
				}
			}
			step += 1;
		}
		console.log(lcmAll(Object.values(repeatIndex)))
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
	const regex = /(-?\d+)/g;
	return raw.split('\n').filter(l => l !== '').map(line => {
		return new Moon(...line.match(regex).map(Number))
	})
}

function simulateStep() {
	let deltas = {}
	for (const [i, m1] of data.entries()) {
		for (const [j, m2] of data.entries()) {
			if (i != j) {
				deltas['' + i + j] = compareTo(m1, m2);
			}
		}
	}
	for (const [key, value] of Object.entries(deltas)) {
		data[Number(key.split('')[0])].applyGravity(...value);
	}
	data.forEach(m => m.applyVelocity());
}

function compareTo(m, otherM) {
	const dx = m.x < otherM.x ? 1 : m.x == otherM.x ? 0 : -1;
	const dy = m.y < otherM.y ? 1 : m.y == otherM.y ? 0 : -1;
	const dz = m.z < otherM.z ? 1 : m.z == otherM.z ? 0 : -1;
	return [dx, dy, dz]
}

function isDone() {
	for (const dim of ['x', 'y', 'z']) {
		if (repeatIndex[dim] === undefined) {
			return false
		}
	}
	return true
}
