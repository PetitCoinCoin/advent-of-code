import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = {};
let portals = {};
let reversePortals = {};
parseInput();
const distances = buildDistances();
switch (argv[2]) {
	case '1':
		console.log(move());
		break
	case '2':
		console.log(move3D());
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
	// Had to add a '#' at 0, 0
	let raw = readInput().split('\n');
	let isLeftStart = true;
	for (const [y, line] of raw.entries()) {
		for (const [x, char] of line.split('').entries()) {
			if (char === '#' || char === ' ') {
				continue
			}
			if (char === '.') {
				data[x + ',' + y] = char;
				continue
			}
			// letter
			const isVertical = (y === 0 || y === raw.length - 1 || (line[x - 1] === ' ' && line[x + 1] === ' ')) ? true : false;
			if (isVertical) {
				const isTopStart = raw[y - 1] === undefined || raw[y - 1][x] === ' ' || raw[y - 1][x] === '.';
				if (isTopStart) {
					const yEntry = raw[y - 1] === undefined || raw[y - 1][x] === ' ' ? y + 2 : y - 1; // up or down
					const level = y === 0 || y === raw.length - 2 ? 1 : -1;  // out or in
					portals[char + raw[y + 1][x]] = (portals[char + raw[y + 1][x]] || []).concat([x + ',' + yEntry + ',' + level]);
					reversePortals[x + ',' + yEntry] = char + raw[y + 1][x];
				}
			} else {
				if (isLeftStart) {
					const xEntry = line[x - 1] === undefined || line[x - 1] === ' ' ? x + 2 : x - 1; // left or rigth
					const level = x === 0 || x === line.length - 2 ? 1 : -1;  // out or in
					portals[char + line[x + 1]] = (portals[char + line[x + 1]] || []).concat([xEntry + ',' + y + ',' + level]);
					reversePortals[xEntry + ',' + y] = char + line[x + 1];
				}
				isLeftStart = !isLeftStart;
			}
		}
	}
}

function sortByDist(a1, a2) {
	if (a1[0] < a2[0]) { return -1 }
	if (a1[0] > a2[0]) { return 1 }
	return 0
}

function buildDistances() {
	let res = {};
	for (const [portal, positions] of Object.entries(portals)) {
		for (const position of positions) {
			const [px, py, ] = position.split(',').map(Number);
			res[[px, py]] = [];
			let queue = [[0, px, py]];
			let seen = {};
			while (queue.length > 0) {
				queue.sort(sortByDist);
				const [dist, x, y] = queue.shift();
				if (reversePortals[x + ',' + y] !== undefined && reversePortals[x + ',' + y] !== portal) {
					res[[px, py]].push([dist, x, y, 0]);
					continue
				}
				if (seen[[x, y]] !== undefined) {
					continue
				}
				seen[[x, y]] = true;
				for (const [dx, dy] of [[0, 1], [0, -1], [1, 0], [-1, 0]]) {
					if (data[[x + dx, y + dy]] !== undefined) {
						queue.push([dist + 1, x + dx, y + dy]);
					}
				}

			}
		}
		if (portal !== 'AA' && portal !== 'ZZ') {
			//add twin portal
			for (const i of [0, 1]) {
				const [px, py, ] = positions[i].split(',').map(Number);
				const [tx, ty, level] = positions[(i + 1) % 2].split(',').map(Number);
				res[[px, py]].push([1, tx, ty, level]);
			}
		}
	}
	return res
}

function move() {
	let queue = [[0, ...portals['AA'][0].split(',').map(Number)]];
	let seen = {};
	const [xZZ, yZZ] = portals['ZZ'][0].split(',').map(Number);
	while (queue.length > 0) {
		queue.sort(sortByDist);
		const [distance, x, y] = queue.shift();
		if (x === xZZ && y === yZZ) {
			return distance
		}
		if (seen[[x, y]] !== undefined) {
			continue
		}
		seen[[x, y]] = true;
		for (const neighbour of distances[[x, y]]) {
			const [delta, nx, ny] = neighbour
			if (seen[[nx, ny]] === undefined) {
				queue.push([distance + delta, nx, ny]);
			}
		}
	}
	return 0
}

function move3D() {
	const [xAA, yAA, ] = portals['AA'][0].split(',').map(Number);
	let queue = [[0, xAA, yAA, 0]];
	let seen = {};
	const [xZZ, yZZ, ] = portals['ZZ'][0].split(',').map(Number);
	while (queue.length > 0) {
		queue.sort(sortByDist);
		const [distance, x, y, level] = queue.shift();
		if (x === xZZ && y === yZZ) {
			return distance
		}
		if (seen[[x, y, level]] !== undefined) {
			continue
		}
		seen[[x, y, level]] = distance;
		for (const neighbour of distances[[x, y]]) {
			const [deltaStep, nx, ny, deltaLevel] = neighbour;
			if (((nx === xAA && ny === yAA) || (nx === xZZ && ny === yZZ)) && level !== 0) {
				continue
			}
			if (seen[[nx, ny, level + deltaLevel]] === undefined && level + deltaLevel >= 0) {
				queue.push([distance + deltaStep, nx, ny, level + deltaLevel]);
			}
		}
	}
	return 0
}
