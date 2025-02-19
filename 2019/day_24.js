import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { range } from '../js_utils/utils.js';

class Bug {
	constructor(r, c, state) {
		this.alive = state;
		this.previous = state;
		this.row = r;
		this.column = c;
	}
	freeze() {
		this.previous = this.alive;
	}
	evolve(grid) {
		const bugs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
		.map(([dr, dc]) => {
			if (grid[this.row + dr] === undefined) {
				return 0
			} 
			if (grid[this.row + dr][this.column + dc] === undefined) {
				return 0
			}
			return (grid[this.row + dr][this.column + dc]).previous ? 1 : 0
		})
		.reduce((tot, val) => tot + val, 0);
		this.update(bugs);
	}
	evolve3D(planet, level) {
		if (this.r == 2 && this.c == 2) {
			return
		}
		let bugs = 0;
		for (const [dr, dc] of [[0, 1], [0, -1], [1, 0], [-1, 0]]) {
			if (this.row + dr === -1) {  // outer grid, top
				if (planet[level - 1] !== undefined) {
					bugs += planet[level - 1][1][2].previous ? 1 : 0;
				}
			} else if (this.row + dr === 5) { // outer grid, bottom
				if (planet[level - 1] !== undefined) {
					bugs += planet[level - 1][3][2].previous ? 1 : 0;
				}
			} else if (this.column + dc === -1) {  // outer grid, left
				if (planet[level - 1] !== undefined) {
					bugs += planet[level - 1][2][1].previous ? 1 : 0;
				}
			} else if (this.column + dc === 5) {  // outer grid, right
				if (planet[level - 1] !== undefined) {
					bugs += planet[level - 1][2][3].previous ? 1 : 0;
				}
			} else if (this.column + dc === 2 && this.row + dr === 2) {
				// inner grid
				/* So I discovered that:
				str - number > number (calculation)
				str + number > str (concatenation)
				Marvellous.
				*/
				if (planet[level - -1] !== undefined) {
					if (dr === 1) {
						bugs += planet[level - -1][0].reduce((tot, b) => tot + (b.previous ? 1 : 0), 0);
					} else if (dr === -1) {
						bugs += planet[level - -1][4].reduce((tot, b) => tot + (b.previous ? 1 : 0), 0);
					} else {
						if (dc === 1) {
							bugs += planet[level - -1].map(row => row[0]).reduce((tot, b) => tot + (b.previous ? 1 : 0), 0);
						} else {
							bugs += planet[level - -1].map(row => row[4]).reduce((tot, b) => tot + (b.previous ? 1 : 0), 0);
						}
					}
				}
			} else {  // nominal
				bugs += planet[level][this.row + dr][this.column + dc].previous ? 1 : 0;
			}
		}
		this.update(bugs);
	}
	update(bugs) {
		if (this.previous && bugs !== 1) {  // this is a bug
			this.alive = false;
		} else if (!this.previous && (bugs === 1 || bugs === 2)) {  // this is an empty space
			this.alive = true;
		}
	}
}

class Grid {
	constructor() {
		this.levels = {0: []};
		this.minLevel = 0;
		this.maxLevel = 0;
	}
	addSpace(r, c, state, level) {
		if (r >= this.levels[level].length) {
			this.levels[level].push([]);
		}
		this.levels[level][r].push(new Bug(r, c, state));
	}
	evolve(isRecursive) {
		if (isRecursive) { this.prepareEvolution() }
		for (const grid of Object.values(this.levels)) {
			grid.forEach(row => {
				row.forEach(bug => bug.freeze());
			})
		}
		for (const [level, grid] of Object.entries(this.levels)) {
			grid.forEach(row => {
				row.forEach(bug => isRecursive ? bug.evolve3D(this.levels, level) : bug.evolve(grid));
			})
		}
	}
	prepareEvolution() {
		if (this.levels[this.minLevel].flat().some(b => b.alive)) {
			this.minLevel--;
			this.levels[this.minLevel] = [...this.initLevel()];
		}
		if (this.levels[this.maxLevel].flat().some(b => b.alive)) {
			this.maxLevel++;
			this.levels[this.maxLevel] = [...this.initLevel()];
		}
	}
	initLevel() {
		let grid = [];
		for (const r of range(0, 5)) {
			grid.push([]);
			for (const c of range(0, 5)) {
				grid[r].push(new Bug(r, c, false));
			}
		}
		return grid
	}
	countBugs() {
		let bugs = 0;
		for (const grid of Object.values(this.levels)) {
			bugs += grid.flat().reduce((tot, b) => tot + (b.alive ? 1 : 0), 0);
			bugs -= grid[2][2].alive ? 1 : 0;
		}
		return bugs
	}
	repr(level) {
		return this.levels[level].flat().map(b => b.alive ? '#' : '.')
	}
}


console.time('run');
let data = new Grid();
parseInput();
switch (argv[2]) {
	case '1':
		let cache = {};
		while (cache[data.repr(0)] === undefined) {
			cache[data.repr(0)] = true;
			data.evolve(false);
		}
		console.log(biodiversityRating());
		break
	case '2':
		for (let i = 0; i < 200; i++) {
			data.evolve(true);
		}
		console.log(data.countBugs());
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
	let raw = readInput().split('\n');
	for (const [r, row] of raw.entries()) {
		for (const [c, char] of row.split('').entries()) {
			data.addSpace(r, c, char === '#', 0);
		}
	}
}

function biodiversityRating() {
	let bio = 0;
	for (const [idx, char] of data.repr(0).entries()) {
		bio += char === '#' ? 2 ** idx : 0
	}
	return bio
}
