// Add your custom JavaScript here 

// Add loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Form validation enhancement
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!this.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        this.classList.add('was-validated');
    });
});

// Dynamic card height adjustment
function adjustCardHeights() {
    const cards = document.querySelectorAll('.election-card');
    let maxHeight = 0;
    
    cards.forEach(card => {
        card.style.height = 'auto';
        maxHeight = Math.max(maxHeight, card.offsetHeight);
    });
    
    cards.forEach(card => {
        card.style.height = maxHeight + 'px';
    });
}

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});

// Initialize popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
});

// Add animation on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('active');
        }
    });
}

// Event listeners
window.addEventListener('load', function() {
    adjustCardHeights();
    animateOnScroll();
});

window.addEventListener('resize', adjustCardHeights);
window.addEventListener('scroll', animateOnScroll);

// Progress bar animation
document.querySelectorAll('.progress-bar').forEach(bar => {
    const width = bar.style.width;
    bar.style.width = '0';
    setTimeout(() => {
        bar.style.width = width;
    }, 100);
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Form validation
    var forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    });

    // Vote form enhancements
    const voteForm = document.querySelector('.vote-form');
    if (voteForm) {
        // Highlight selected candidate
        const radioInputs = voteForm.querySelectorAll('input[type="radio"]');
        radioInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Remove highlight from all cards in this position group
                const positionCards = this.closest('.position-group').querySelectorAll('.candidate-card');
                positionCards.forEach(card => card.classList.remove('selected'));
                
                // Add highlight to selected card
                if (this.checked) {
                    this.closest('.candidate-card').classList.add('selected');
                }
            });
        });

        // Progress tracking
        function updateProgress() {
            const total = document.querySelectorAll('.position-group').length;
            const completed = document.querySelectorAll('input[type="radio"]:checked').length;
            const progressBar = document.querySelector('.vote-progress .progress-bar');
            const percentage = (completed / total) * 100;
            
            progressBar.style.width = percentage + '%';
            progressBar.setAttribute('aria-valuenow', percentage);
            
            document.querySelector('.progress-text').textContent = 
                `${completed} of ${total} positions selected`;
                
            // Enable/disable submit button
            const submitBtn = document.querySelector('.submit-vote-btn');
            submitBtn.disabled = completed < total;
        }

        voteForm.querySelectorAll('input[type="radio"]').forEach(input => {
            input.addEventListener('change', updateProgress);
        });
        
        // Initial progress check
        updateProgress();
    }

    // Results animation
    const resultBars = document.querySelectorAll('.result-bar');
    if (resultBars.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        });

        resultBars.forEach(bar => observer.observe(bar));
    }
}); 