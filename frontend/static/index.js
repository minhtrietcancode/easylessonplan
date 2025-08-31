/**
 * EasyLesson Frontend JavaScript
 * Handles UI interactions, authentication, and visual effects for the home page
 */

class AuthManager {
    /**
     * Manages authentication-related functionality
     */
    
    static async checkAuthStatus() {
        try {
            const response = await fetch('/auth/user');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.warn('Auth status check failed:', error.message);
            return { user: null, authenticated: false };
        }
    }
    
    static updateUIForLoggedInUser(user) {
        const authButtons = document.querySelectorAll('[id^="google-auth-button"]');
        
        authButtons.forEach(button => {
            // Update button content to show user info
            button.innerHTML = `
                <i class="fas fa-user-circle"></i> 
                Welcome, ${this.getFirstName(user.name)}
            `;
            
            // Update click behavior to go to dashboard
            button.onclick = (e) => {
                e.preventDefault();
                window.location.href = '/dashboard';
            };
            
            // Update accessibility
            button.setAttribute('aria-label', `Go to dashboard, ${user.name}`);
        });
    }
    
    static updateUIForGuestUser() {
        const authButtons = document.querySelectorAll('[id^="google-auth-button"]');
        
        authButtons.forEach(button => {
            // Reset to login button
            button.innerHTML = `
                <i class="fab fa-google"></i> 
                Continue with Google
            `;
            
            // Update click behavior to start login
            button.onclick = (e) => {
                e.preventDefault();
                window.location.href = '/auth/login';
            };
            
            // Update accessibility
            button.setAttribute('aria-label', 'Sign in with Google');
        });
    }
    
    static getFirstName(fullName) {
        return fullName ? fullName.split(' ')[0] : 'User';
    }
    
    static async initialize() {
        const authData = await this.checkAuthStatus();
        
        if (authData.user) {
            this.updateUIForLoggedInUser(authData.user);
        } else {
            this.updateUIForGuestUser();
        }
        
        return authData;
    }
}


class UIAnimations {
    /**
     * Handles visual animations and effects
     */
    
    static initializeScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Apply fade-in animation to feature cards
        document.querySelectorAll('.feature-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease';
            observer.observe(card);
        });
    }
    
    static initializeParallaxEffect() {
        const hero = document.querySelector('.hero');
        if (!hero) return;
        
        let ticking = false;
        
        const updateParallax = () => {
            const scrolled = window.pageYOffset;
            hero.style.transform = `translateY(${scrolled * 0.1}px)`;
            ticking = false;
        };
        
        const requestParallaxUpdate = () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        };
        
        window.addEventListener('scroll', requestParallaxUpdate, { passive: true });
    }
    
    static initializeSmoothScrolling() {
        document.querySelectorAll('.nav-links a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    static initialize() {
        this.initializeScrollAnimations();
        this.initializeParallaxEffect();
        this.initializeSmoothScrolling();
    }
}


class EventHandlers {
    /**
     * Manages event listeners and user interactions
     */
    
    static initializeAuthButtons() {
        // Auth buttons are handled by AuthManager.initialize()
        // This method can be extended for additional auth-related events
        
        // Add keyboard accessibility for auth buttons
        document.querySelectorAll('[id^="google-auth-button"]').forEach(button => {
            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    button.click();
                }
            });
        });
    }
    
    static initializeFormValidation() {
        // Placeholder for future form validation if needed
        // Can be extended when adding contact forms or other inputs
    }
    
    static handleNavigationInteractions() {
        // Add active state handling for navigation
        const navLinks = document.querySelectorAll('.nav-links a');
        
        navLinks.forEach(link => {
            link.addEventListener('focus', () => {
                link.style.outline = '2px solid #4C50CC';
                link.style.outlineOffset = '2px';
            });
            
            link.addEventListener('blur', () => {
                link.style.outline = 'none';
            });
        });
    }
    
    static initialize() {
        this.initializeAuthButtons();
        this.initializeFormValidation();
        this.handleNavigationInteractions();
    }
}


class AppInitializer {
    /**
     * Main application initializer that coordinates all modules
     */
    
    static async initialize() {
        try {
            console.log('🚀 Initializing EasyLesson frontend...');
            
            // Initialize UI animations and effects
            UIAnimations.initialize();
            
            // Initialize event handlers
            EventHandlers.initialize();
            
            // Initialize authentication and update UI
            const authData = await AuthManager.initialize();
            
            console.log('✅ Frontend initialization complete');
            console.log('👤 Auth status:', authData.authenticated ? 'Logged in' : 'Guest');
            
        } catch (error) {
            console.error('❌ Frontend initialization failed:', error);
            // Show user-friendly error message
            this.showInitializationError();
        }
    }
    
    static showInitializationError() {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        errorDiv.textContent = 'Some features may not work properly. Please refresh the page.';
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}


// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    AppInitializer.initialize();
});

// Handle page visibility changes (for auth status refresh)
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Page became visible, refresh auth status
        AuthManager.initialize();
    }
});

// Export modules for potential use by other scripts
window.EasyLessonApp = {
    AuthManager,
    UIAnimations,
    EventHandlers,
    AppInitializer
};