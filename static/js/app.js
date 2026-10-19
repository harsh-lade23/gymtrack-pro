/**
 * GymTrack Pro — Frontend JavaScript
 * Handles Modals, AJAX requests, Dynamic Form Inputs, and Toast Notifications
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash messages after 4 seconds
    const flashMessages = document.querySelectorAll('.flash-msg');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(50px)';
            msg.style.transition = 'all 0.4s ease';
            setTimeout(() => msg.remove(), 400);
        }, 4000);
    });

    // Close modal when clicking on overlay background
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                closeModal(overlay.id);
            }
        });
    });

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.active').forEach(overlay => {
                closeModal(overlay.id);
            });
        }
    });
});

/**
 * Open a modal by ID
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

/**
 * Close a modal by ID
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

/**
 * Populate and open Edit Member Modal
 */
function openEditMemberModal(id, name, phone, age, weight, status, trainer) {
    const form = document.getElementById('editMemberForm');
    if (form) {
        form.action = `/members/update/${id}`;
        document.getElementById('edit_name').value = name;
        document.getElementById('edit_phone').value = phone;
        document.getElementById('edit_age').value = age;
        document.getElementById('edit_weight').value = weight;
        document.getElementById('edit_status').value = status;
        document.getElementById('edit_trainer').value = trainer;
        openModal('editMemberModal');
    }
}

/**
 * Populate and open Edit Trainer Modal
 */
function openEditTrainerModal(id, name, phone, exp, rating, salary) {
    const form = document.getElementById('editTrainerForm');
    if (form) {
        form.action = `/trainers/update/${id}`;
        document.getElementById('edit_trainer_name').textContent = name;
        document.getElementById('edit_trainer_phone').value = phone;
        document.getElementById('edit_trainer_exp').value = exp;
        document.getElementById('edit_trainer_rating').value = rating;
        document.getElementById('edit_trainer_salary').value = salary;
        openModal('editTrainerModal');
    }
}

/**
 * Add exercise row dynamically in Workout Modal
 */
function addExerciseRow() {
    const container = document.getElementById('exerciseRows');
    if (!container) return;
    const row = document.createElement('div');
    row.className = 'form-row-3 mb-1 exercise-item align-center';
    row.style.gap = '10px';
    row.innerHTML = `
        <div style="flex: 2;">
            <input type="text" name="ex_name[]" class="form-control" placeholder="e.g. Bench Press" required>
        </div>
        <div style="flex: 1;">
            <input type="number" name="ex_sets[]" class="form-control" placeholder="Sets" value="3" min="1" required>
        </div>
        <div style="flex: 1;">
            <input type="number" name="ex_reps[]" class="form-control" placeholder="Reps" value="10" min="1" required>
        </div>
        <div style="flex: 1;">
            <input type="number" step="0.5" name="ex_weight[]" class="form-control" placeholder="Kg" value="40">
        </div>
        <div>
            <button type="button" class="btn-icon danger" onclick="this.closest('.exercise-item').remove()" title="Remove">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    container.appendChild(row);
}

/**
 * Open Add Exercise to Existing Workout Modal
 */
function openAddExerciseModal(workoutId, memberName) {
    const form = document.getElementById('addExerciseForm');
    if (form) {
        form.action = `/workouts/add-exercise/${workoutId}`;
        const label = document.getElementById('addExerciseMemberName');
        if (label) label.textContent = memberName;
        openModal('addExerciseModal');
    }
}

/**
 * Run explain() query test via AJAX
 */
async function runExplainQuery(type) {
    const outputEl = document.getElementById('explainOutput');
    const badgeEl = document.getElementById('explainStage');
    const timeEl = document.getElementById('explainTime');
    const docsEl = document.getElementById('explainDocs');
    const indexEl = document.getElementById('explainIndex');

    if (outputEl) outputEl.textContent = 'Running db.collection.find().explain()...';

    try {
        const res = await fetch(`/indexes/explain?type=${type}`);
        const data = await res.json();

        if (data.success) {
            const exp = data.explain;
            if (badgeEl) badgeEl.textContent = exp.stage;
            if (timeEl) timeEl.textContent = `${exp.execution_time} ms`;
            if (docsEl) docsEl.textContent = `${exp.docs_examined} docs examined (${exp.docs_returned} returned)`;
            if (indexEl) indexEl.textContent = exp.index_used;

            if (outputEl) {
                outputEl.textContent = exp.winning_plan;
            }
        } else {
            if (outputEl) outputEl.textContent = `Error: ${data.error}`;
        }
    } catch (err) {
        if (outputEl) outputEl.textContent = `Request failed: ${err.message}`;
    }
}

/**
 * Run schema validation test via AJAX
 */
async function testSchemaValidation(testType) {
    const resultBox = document.getElementById('validationResultBox');
    if (!resultBox) return;

    resultBox.className = 'validation-result show';
    resultBox.textContent = 'Submitting document to MongoDB collection...';

    const formData = new FormData();
    formData.append('test_type', testType);

    try {
        const res = await fetch('/validation/test', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        resultBox.classList.remove('valid', 'invalid');
        if (data.success) {
            resultBox.classList.add('valid');
        } else {
            resultBox.classList.add('invalid');
        }
        resultBox.textContent = data.message;
    } catch (err) {
        resultBox.className = 'validation-result show invalid';
        resultBox.textContent = `Network / Request Error: ${err.message}`;
    }
}
