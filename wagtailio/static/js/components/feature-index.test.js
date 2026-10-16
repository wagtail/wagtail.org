import FeatureIndex from './feature-index';

const render = () => {
    document.body.innerHTML = `
        <div data-feature-index>
            <input type="checkbox" id="all" data-filter-all checked />
            <input type="checkbox" id="editors" data-filter="editors" />
            <input type="checkbox" id="developers" data-filter="developers" />
            <div data-feature-group="editors"></div>
            <div data-feature-group="developers"></div>
        </div>`;
    // eslint-disable-next-line no-new
    new FeatureIndex(document.querySelector('[data-feature-index]'));
};

const toggle = (id, checked) => {
    const input = document.getElementById(id);
    input.checked = checked;
    input.dispatchEvent(new Event('change'));
};

const isHidden = (group) =>
    document
        .querySelector(`[data-feature-group="${group}"]`)
        .classList.contains('is-hidden');

describe('FeatureIndex', () => {
    beforeEach(render);

    it('shows only the ticked group and unticks "All"', () => {
        toggle('editors', true);

        expect(document.getElementById('all').checked).toBe(false);
        expect(isHidden('editors')).toBe(false);
        expect(isHidden('developers')).toBe(true);
    });

    it('shows every group again when the last filter is unticked', () => {
        toggle('editors', true);
        toggle('editors', false);

        expect(document.getElementById('all').checked).toBe(true);
        expect(isHidden('editors')).toBe(false);
        expect(isHidden('developers')).toBe(false);
    });

    it('clears the filters when "All" is ticked', () => {
        toggle('editors', true);
        toggle('all', true);

        expect(document.getElementById('editors').checked).toBe(false);
        expect(isHidden('developers')).toBe(false);
    });

    it('keeps "All" ticked when it is the only thing ticked', () => {
        toggle('all', false);

        expect(document.getElementById('all').checked).toBe(true);
    });
});
