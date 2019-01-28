import {greeter} from '../src/index';

describe('greater', () => {
    it('yunabe', () => {
        expect(greeter('yunabe')).toBe('Hello, yunabe');
    });
});
