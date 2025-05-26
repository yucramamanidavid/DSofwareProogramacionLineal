document.addEventListener('DOMContentLoaded', () => {
    const agregarBtn = document.querySelector('#btn-agregar-restriccion');
    const contenedor = document.querySelector('#restricciones');
    let restriccionCount = contenedor?.children.length || 1;

    if (agregarBtn) {
        agregarBtn.addEventListener('click', () => {
            restriccionCount++;
            const div = document.createElement('div');
            div.classList.add('restriccion');
            div.innerHTML = `
                <input type="number" step="any" name="a[]" placeholder="Coef. x₁" required>
                x₁ +
                <input type="number" step="any" name="b[]" placeholder="Coef. x₂" required>
                x₂
                <select name="signo[]">
                    <option value="<=">&le;</option>
                    <option value=">=">&ge;</option>
                    <option value="=">=</option>
                </select>
                <input type="number" step="any" name="rhs[]" placeholder="RHS" required>
                ${restriccionCount > 1 ? `<button type="button" class="btn btn-danger btn-sm eliminar" onclick="this.parentElement.remove()">×</button>` : ''}
            `;
            contenedor.appendChild(div);
        });
    }

    const form = document.querySelector('form');
    const loading = document.querySelector('#loading');
    if (form && loading) {
        form.addEventListener('submit', () => {
            loading.style.display = 'block';
        });
    }
});
