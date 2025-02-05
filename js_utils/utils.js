const permute = (permutation) => {
	// Thanks to https://stackoverflow.com/a/37580979
	var length = permutation.length,
		result = [permutation.slice()],
		c = new Array(length).fill(0),
		i = 1, k, p;

	while (i < length) {
		if (c[i] < i) {
			k = i % 2 && c[i];
			p = permutation[i];
			permutation[i] = permutation[k];
			permutation[k] = p;
			++c[i];
			i = 1;
			result.push(permutation.slice());
		} else {
			c[i] = 0;
			++i;
		}
	}
	return result;
}

const range = (startRange, endRange, step = 1) => {
	return Array.from({length: Math.abs(endRange - startRange)}, (_, i) => i * step + startRange)
}

const manhattan = (p1, p2) => {
	return Math.abs(p1.x - p2.x) + Math.abs(p1.y - p2.y)
}

const gcd = (a, b) => b == 0 ? a : gcd (b, a % b)
const lcm = (a, b) =>  a / gcd (a, b) * b
const lcmAll = (ns) => ns.reduce (lcm, 1)

const Point = class Point {
	constructor(x, y) {
		this.x = x;
		this.y = y;
	}

	getNeighbours() {
		return [[0, 1], [0, -1], [1, 0], [-1, 0]].map(([dx, dy]) => Point(this.x + dx, this.y + dy))
	}
}

export { gcd, lcm, lcmAll, manhattan, permute, range, Point };
