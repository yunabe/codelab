import {greeter} from './index';

describe('greater', () => {
    it('yunabe', () => {
        expect(greeter('yunabe')).toBe('Hello, yunabe');
    });
});
