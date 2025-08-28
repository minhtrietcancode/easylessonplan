// Add smooth scrolling and interactive effects
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    checkAuthStatus();
    
    // Smooth reveal animation for feature cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // Google Auth button click handlers
    document.querySelectorAll('[id^="google-auth-button"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // Redirect to Flask backend authentication route
            window.location.href = '/auth/login';
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-links a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.hash;
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add parallax effect to hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.1}px)`;
        }
    });
});

// Check authentication status
async function checkAuthStatus() {
    try {
        const response = await fetch('/auth/user');
        const data = await response.json();
        
        if (data.user) {
            // User is logged in, update UI accordingly
            updateUIForLoggedInUser(data.user);
        }
    } catch (error) {
        console.log('Auth check failed:', error);
    }
}

// Update UI for logged-in user
function updateUIForLoggedInUser(user) {
    // Update Google auth buttons to show user info or dashboard link
    document.querySelectorAll('[id^="google-auth-button"]').forEach(button => {
        button.innerHTML = `
            <i class="fas fa-user-circle"></i> 
            Welcome, ${user.name.split(' ')[0]}
        `;
        button.onclick = function(e) {
            e.preventDefault();
            window.location.href = '/dashboard';
        };
    });
}