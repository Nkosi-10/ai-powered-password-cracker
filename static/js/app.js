/**
 * AI-Powered Password Cracker Simulator - Frontend JavaScript
 * 
 * Handles all user interactions, API calls, and UI updates
 */

class PasswordCrackerApp {
    constructor() {
        this.currentAttack = null;
        this.fakePasswords = [];
        this.systemStatus = {
            backend: false,
            ai: false,
            fakeData: false
        };
        
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Password Cracker App...');
        
        // Initialize UI elements
        this.initializeUI();
        
        // Check system status
        await this.checkSystemStatus();
        
        // Load fake passwords
        await this.loadFakePasswords();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Matrix effect removed for cleaner UI
        
        console.log('✅ App initialized successfully');
    }

    initializeUI() {
        // Get DOM elements
        this.elements = {
            targetHash: document.getElementById('targetHash'),
            attackMethod: document.getElementById('attackMethod'),
            methodOptions: document.getElementById('methodOptions'),
            bruteForceOptions: document.getElementById('bruteForceOptions'),
            aiOptions: document.getElementById('aiOptions'),
            maxLength: document.getElementById('maxLength'),
            maxLengthValue: document.getElementById('maxLengthValue'),
            context: document.getElementById('context'),
            quickPassword: document.getElementById('quickPassword'),
            startAttack: document.getElementById('startAttack'),
            validateHash: document.getElementById('validateHash'),
            generateHash: document.getElementById('generateHash'),
            attackProgress: document.getElementById('attackProgress'),
            progressBar: document.getElementById('progressBar'),
            progressText: document.getElementById('progressText'),
            resultsDisplay: document.getElementById('resultsDisplay'),
            fakeHashesList: document.getElementById('fakeHashesList'),
            aiStatus: document.getElementById('aiStatus'),
            aiStatusDetail: document.getElementById('aiStatusDetail'),
            fakeDataStatus: document.getElementById('fakeDataStatus'),
            lastUpdate: document.getElementById('lastUpdate'),
            loadingModal: new bootstrap.Modal(document.getElementById('loadingModal')),
            modalProgressBar: document.getElementById('modalProgressBar')
        };

        // Set up method-specific options
        this.setupMethodOptions();
    }

    setupMethodOptions() {
        this.elements.attackMethod.addEventListener('change', (e) => {
            const method = e.target.value;
            
            // Hide all options
            this.elements.bruteForceOptions.classList.add('d-none');
            this.elements.aiOptions.classList.add('d-none');
            
            // Show relevant options
            if (method === 'brute_force') {
                this.elements.bruteForceOptions.classList.remove('d-none');
            } else if (method === 'ai') {
                this.elements.aiOptions.classList.remove('d-none');
            }
        });

        // Set up brute force length slider
        this.elements.maxLength.addEventListener('input', (e) => {
            this.elements.maxLengthValue.textContent = e.target.value;
        });
    }

    setupEventListeners() {
        // Hash validation
        this.elements.validateHash.addEventListener('click', () => {
            this.validateHash();
        });

        // Hash generation
        this.elements.generateHash.addEventListener('click', () => {
            this.generateHash();
        });

        // Attack button
        this.elements.startAttack.addEventListener('click', () => {
            this.startAttack();
        });

        // Input validation for attack button
        this.elements.targetHash.addEventListener('input', () => {
            this.validateAttackButton();
        });

        // Enter key support
        this.elements.targetHash.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.startAttack();
            }
        });

        this.elements.quickPassword.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.generateHash();
            }
        });

        // API data fetch button
        const fetchApiDataBtn = document.getElementById('fetchApiData');
        if (fetchApiDataBtn) {
            fetchApiDataBtn.addEventListener('click', () => {
                this.fetchApiData();
            });
        }
    }

    async checkSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            this.systemStatus.backend = true;
            this.systemStatus.ai = data.ai_available;
            this.systemStatus.fakeData = data.fake_passwords_count > 0;
            
            // Update UI
            this.updateSystemStatus();
            
        } catch (error) {
            console.error('❌ Failed to check system status:', error);
            this.systemStatus.backend = false;
            this.updateSystemStatus();
        }
    }

    async loadFakePasswords() {
        try {
            const response = await fetch('/api/fake-passwords');
            const data = await response.json();
            
            this.fakePasswords = data.passwords;
            this.renderFakePasswords();
            
        } catch (error) {
            console.error('❌ Failed to load fake passwords:', error);
        }
    }

    renderFakePasswords() {
        const container = this.elements.fakeHashesList;
        container.innerHTML = '';

        this.fakePasswords.forEach((item, index) => {
            const listItem = document.createElement('div');
            listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
            listItem.style.background = 'transparent';
            listItem.style.border = '1px solid var(--hacker-green)';
            listItem.style.color = 'var(--text-primary)';
            listItem.style.marginBottom = '5px';
            listItem.style.borderRadius = '5px';
            listItem.style.cursor = 'pointer';
            
            listItem.innerHTML = `
                <div>
                    <strong>Hash:</strong> <code>${item.hash.substring(0, 16)}...</code>
                    <br>
                    <small class="text-secondary">${item.description}</small>
                </div>
                <button class="btn btn-sm btn-outline-success" onclick="app.useFakeHash('${item.hash}')">
                    <i class="fas fa-copy"></i>
                </button>
            `;
            
            container.appendChild(listItem);
        });
    }

    useFakeHash(hash) {
        this.elements.targetHash.value = hash;
        this.validateAttackButton();
        this.showNotification('Hash copied to input field', 'success');
    }

    async validateHash() {
        const hash = this.elements.targetHash.value.trim();
        
        if (!hash) {
            this.showNotification('Please enter a hash to validate', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/validate-hash', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ hash })
            });

            const data = await response.json();
            
            if (data.error) {
                this.showNotification(data.message, 'error');
                return;
            }

            if (data.is_suspicious) {
                this.showNotification(`⚠️ Warning: ${data.warning}`, 'warning');
            } else if (data.is_valid) {
                this.showNotification('✅ Hash format is valid', 'success');
            } else {
                this.showNotification('❌ Invalid hash format', 'error');
            }

        } catch (error) {
            console.error('❌ Hash validation failed:', error);
            this.showNotification('Failed to validate hash', 'error');
        }
    }

    async generateHash() {
        const password = this.elements.quickPassword.value.trim();
        
        if (!password) {
            this.showNotification('Please enter a password to hash', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/generate-hash', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ password })
            });

            const data = await response.json();
            
            if (data.error) {
                this.showNotification(data.message, 'error');
                return;
            }

            // Copy hash to target field
            this.elements.targetHash.value = data.hash;
            this.validateAttackButton();
            
            this.showNotification(`Hash generated`, 'success');
            
            // Clear password field
            this.elements.quickPassword.value = '';

        } catch (error) {
            console.error('❌ Hash generation failed:', error);
            this.showNotification('Failed to generate hash', 'error');
        }
    }

    validateAttackButton() {
        const hash = this.elements.targetHash.value.trim();
        const method = this.elements.attackMethod.value;
        
        let isValid = hash.length >= 32; // Minimum hash length
        
        // Additional validation for brute force
        if (method === 'brute_force') {
            const maxLength = parseInt(this.elements.maxLength.value);
            isValid = isValid && maxLength >= 1 && maxLength <= 6;
        }
        
        this.elements.startAttack.disabled = !isValid;
    }

    async startAttack() {
        const hash = this.elements.targetHash.value.trim();
        const method = this.elements.attackMethod.value;
        const context = this.elements.context?.value?.trim() || '';
        const maxLength = parseInt(this.elements.maxLength?.value || '4');

        if (!hash) {
            this.showNotification('Please enter a target hash', 'warning');
            return;
        }

        // Prepare attack data
        const attackData = {
            target_hash: hash,
            method: method
        };

        if (method === 'brute_force') {
            attackData.max_length = maxLength;
        }

        if (method === 'ai' && context) {
            attackData.context = context;
        }

        // Show loading modal
        this.elements.loadingModal.show();
        
        // Start progress simulation
        this.simulateProgress();

        try {
            console.log(`🚀 Starting ${method} attack on hash: ${hash.substring(0, 16)}...`);
            
            const response = await fetch('/api/attack', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(attackData)
            });

            const result = await response.json();
            
            // Hide loading modal
            this.elements.loadingModal.hide();
            
            // Display results
            this.displayResults(result);
            
            // Update last update time
            this.updateLastUpdate();
            
        } catch (error) {
            console.error('❌ Attack failed:', error);
            this.elements.loadingModal.hide();
            this.showNotification('Attack failed: ' + error.message, 'error');
        }
    }

    simulateProgress() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            
            this.elements.modalProgressBar.style.width = progress + '%';
            
            if (progress >= 90) {
                clearInterval(interval);
            }
        }, 200);
    }

    displayResults(result) {
        const container = this.elements.resultsDisplay;
        
        if (result.error) {
            container.innerHTML = `
                <div class="alert alert-danger result-failure">
                    <h5><i class="fas fa-exclamation-triangle"></i> Attack Failed</h5>
                    <p class="mb-0">${result.error}</p>
                </div>
            `;
            return;
        }

        const successClass = result.success ? 'result-success' : 'result-failure';
        const successIcon = result.success ? 'fa-check-circle' : 'fa-times-circle';
        const successText = result.success ? 'SUCCESS' : 'FAILED';
        const successColor = result.success ? 'text-success' : 'text-danger';

        let statsHtml = '';
        if (result.stats) {
            const stats = result.stats;
            statsHtml = `
                <div class="mt-3">
                    <h6>Attack Statistics:</h6>
                    <div class="row">
                        <div class="col-6">
                            <small class="text-secondary">Method:</small><br>
                            <strong>${stats.method || 'Unknown'}</strong>
                        </div>
                        <div class="col-6">
                            <small class="text-secondary">Attempts:</small><br>
                            <strong>${result.attempts?.toLocaleString() || '0'}</strong>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-6">
                            <small class="text-secondary">Time:</small><br>
                            <strong>${result.time_taken?.toFixed(3) || '0'}s</strong>
                        </div>
                        <div class="col-6">
                            <small class="text-secondary">Rate:</small><br>
                            <strong>${result.attempts && result.time_taken ? Math.round(result.attempts / result.time_taken).toLocaleString() : '0'}/s</strong>
                        </div>
                    </div>
                </div>
            `;
        }

        // AI insights
        let aiInsightsHtml = '';
        if (result.method === 'ai' && result.stats?.ai_analysis) {
            const analysis = result.stats.ai_analysis;
            aiInsightsHtml = `
                <div class="mt-3 p-3" style="background: rgba(0, 255, 65, 0.1); border: 1px solid var(--hacker-green); border-radius: 5px;">
                    <h6><i class="fas fa-brain"></i> AI Insights:</h6>
                    <div class="row">
                        <div class="col-6">
                            <small class="text-secondary">Recommendation:</small><br>
                            <strong>${analysis.recommendation || 'N/A'}</strong>
                        </div>
                        <div class="col-6">
                            <small class="text-secondary">Probability:</small><br>
                            <strong>${analysis.probability || 'N/A'}</strong>
                        </div>
                    </div>
                    <div class="mt-2">
                        <small class="text-secondary">Reasoning:</small><br>
                        <small>${analysis.reasoning || 'N/A'}</small>
                    </div>
                </div>
            `;
        }

        container.innerHTML = `
            <div class="alert ${successClass}">
                <h5>
                    <i class="fas ${successIcon} ${successColor}"></i>
                    Attack ${successText}
                </h5>
                
                ${result.success ? `
                    <div class="alert alert-success">
                        <strong>Password Found:</strong> <code>${result.password_masked}</code>
                    </div>
                ` : `
                    <div class="alert alert-warning">
                        <strong>Password not found</strong> using ${result.method} method
                    </div>
                `}
                
                <div class="row">
                    <div class="col-6">
                        <strong>Method:</strong> ${result.method.replace('_', ' ').toUpperCase()}
                    </div>
                    <div class="col-6">
                        <strong>Time:</strong> ${result.time_taken?.toFixed(3) || '0'} seconds
                    </div>
                </div>
                
                <div class="row mt-2">
                    <div class="col-6">
                        <strong>Attempts:</strong> ${result.attempts?.toLocaleString() || '0'}
                    </div>
                    <div class="col-6">
                        <strong>Hash:</strong> <code>${result.target_hash.substring(0, 16)}...</code>
                    </div>
                </div>
                
                ${statsHtml}
                ${aiInsightsHtml}
            </div>
        `;
    }

    updateSystemStatus() {
        // Update AI status
        if (this.systemStatus.ai) {
            this.elements.aiStatus.textContent = 'Available';
            this.elements.aiStatusDetail.textContent = 'Online';
            this.elements.aiStatusDetail.className = 'text-success';
        } else {
            this.elements.aiStatus.textContent = 'Unavailable';
            this.elements.aiStatusDetail.textContent = 'Offline - API key required';
            this.elements.aiStatusDetail.className = 'text-warning';
        }

        // Update fake data status
        if (this.systemStatus.fakeData) {
            this.elements.fakeDataStatus.textContent = `${this.fakePasswords.length} passwords loaded`;
        } else {
            this.elements.fakeDataStatus.textContent = 'No data available';
        }

        // Update last update time
        this.updateLastUpdate();
    }

    updateLastUpdate() {
        const now = new Date();
        this.elements.lastUpdate.textContent = now.toLocaleTimeString();
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            animation: slideIn 0.3s ease;
        `;
        
        notification.innerHTML = `
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    async fetchApiData() {
        try {
            console.log('🔄 Fetching data from secure API endpoint...');
            
            const fetchBtn = document.getElementById('fetchApiData');
            const originalText = fetchBtn.innerHTML;
            
            // Show loading state
            fetchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            fetchBtn.disabled = true;
            
            const response = await fetch('/data');
            const data = await response.json();
            
            // Display the API response
            this.displayApiData(data);
            
            // Reset button
            fetchBtn.innerHTML = originalText;
            fetchBtn.disabled = false;
            
            if (data.success) {
                this.showNotification('✅ API data fetched successfully', 'success');
            } else {
                this.showNotification('❌ Failed to fetch API data', 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to fetch API data:', error);
            this.showNotification('Failed to fetch API data: ' + error.message, 'error');
            
            // Reset button on error
            const fetchBtn = document.getElementById('fetchApiData');
            fetchBtn.innerHTML = '<i class="fas fa-download"></i> Fetch API Data';
            fetchBtn.disabled = false;
        }
    }

    displayApiData(data) {
        const display = document.getElementById('apiDataDisplay');
        const content = document.getElementById('apiDataContent');
        
        if (data.error) {
            content.textContent = `Error: ${data.message}`;
            content.className = 'text-danger';
        } else {
            // Format the JSON response nicely
            content.textContent = JSON.stringify(data, null, 2);
            content.className = 'text-success';
        }
        
        display.classList.remove('d-none');
    }

    startMatrixEffect() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const matrixBg = document.getElementById('matrixBg');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        matrixBg.appendChild(canvas);
        
        const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
        const matrixArray = matrix.split("");
        
        const fontSize = 10;
        const columns = canvas.width / fontSize;
        
        const drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }
        
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        setInterval(draw, 35);
        
        // Resize handler
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }

    // USB Device Simulation Functions
    async createUSBDevice() {
        const deviceType = this.elements.deviceType.value;
        const securityLevel = this.elements.securityLevel.value;
        const customPassword = this.elements.customPassword.value.trim();

        const deviceData = {
            device_type: deviceType,
            security_level: securityLevel
        };

        if (customPassword) {
            deviceData.password = customPassword;
        }

        try {
            console.log(`🔧 Creating simulated ${deviceType} with ${securityLevel} security...`);
            
            const response = await fetch('/api/usb/devices', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(deviceData)
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ ${result.message}`, 'success');
                this.elements.customPassword.value = '';
                this.listUSBDevices(); // Refresh device list
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to create device:', error);
            this.showNotification('Failed to create device: ' + error.message, 'error');
        }
    }

    async quickUSBSetup() {
        try {
            console.log('🚀 Setting up pre-configured USB devices...');
            
            const response = await fetch('/api/usb/quick-setup', {
                method: 'POST'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ ${result.message}`, 'success');
                this.listUSBDevices(); // Refresh device list
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to setup devices:', error);
            this.showNotification('Failed to setup devices: ' + error.message, 'error');
        }
    }

    async listUSBDevices() {
        try {
            console.log('📋 Fetching USB devices...');
            
            const response = await fetch('/api/usb/devices');
            const result = await response.json();
            
            if (result.success) {
                this.displayUSBDevices(result.devices);
                this.elements.usbDeviceList.style.display = 'block';
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to list devices:', error);
            this.showNotification('Failed to list devices: ' + error.message, 'error');
        }
    }

    displayUSBDevices(devices) {
        const container = this.elements.usbDevices;
        container.innerHTML = '';

        if (devices.length === 0) {
            container.innerHTML = '<div class="col-12"><p class="text-muted">No devices found. Create some devices first!</p></div>';
            return;
        }

        devices.forEach(device => {
            const deviceCard = document.createElement('div');
            deviceCard.className = 'col-md-6 col-lg-4 mb-3';
            
            const statusClass = device.is_locked ? 'text-danger' : 'text-success';
            const statusIcon = device.is_locked ? 'fa-lock' : 'fa-unlock';
            
            deviceCard.innerHTML = `
                <div class="card hacker-card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">
                            <i class="fas fa-${this.getDeviceIcon(device.device_type)}"></i>
                            ${device.device_type.replace('_', ' ').toUpperCase()}
                        </h6>
                        <span class="badge bg-${this.getSecurityBadgeColor(device.security_level)}">
                            ${device.security_level}
                        </span>
                    </div>
                    <div class="card-body">
                        <p class="card-text small">
                            <strong>ID:</strong> ${device.device_id.substring(0, 12)}...<br>
                            <strong>Algorithm:</strong> ${device.encryption_algorithm}<br>
                            <strong>Status:</strong> 
                            <span class="${statusClass}">
                                <i class="fas ${statusIcon}"></i>
                                ${device.is_locked ? 'Locked' : 'Unlocked'}
                            </span><br>
                            <strong>Attempts:</strong> ${device.failed_attempts}/${device.max_attempts}
                        </p>
                        <div class="d-grid gap-2">
                            <button class="btn btn-sm btn-outline-info" onclick="app.detectUSBDeviceById('${device.device_id}')">
                                <i class="fas fa-search"></i> Detect
                            </button>
                            <button class="btn btn-sm btn-outline-warning" onclick="app.resetUSBDevice('${device.device_id}')">
                                <i class="fas fa-redo"></i> Reset
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            container.appendChild(deviceCard);
        });
    }

    getDeviceIcon(deviceType) {
        const icons = {
            'flash_drive': 'usb',
            'external_hdd': 'hdd',
            'usb_ssd': 'ssd',
            'encrypted_device': 'shield-alt',
            'smart_card': 'credit-card'
        };
        return icons[deviceType] || 'usb';
    }

    getSecurityBadgeColor(securityLevel) {
        const colors = {
            'basic': 'secondary',
            'standard': 'info',
            'advanced': 'warning',
            'military': 'danger'
        };
        return colors[securityLevel] || 'secondary';
    }

    async detectUSBDevice() {
        const deviceId = this.elements.detectDeviceId.value.trim();
        
        if (!deviceId) {
            this.showNotification('Please enter a device ID', 'warning');
            return;
        }

        try {
            console.log(`🔍 Detecting device: ${deviceId}...`);
            
            const response = await fetch(`/api/usb/devices/${deviceId}/detect`, {
                method: 'POST'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ ${result.message}`, 'success');
                this.displayUSBResult(result);
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to detect device:', error);
            this.showNotification('Failed to detect device: ' + error.message, 'error');
        }
    }

    async detectUSBDeviceById(deviceId) {
        this.elements.detectDeviceId.value = deviceId;
        await this.detectUSBDevice();
    }

    async unlockUSBDevice() {
        const deviceId = this.elements.unlockDeviceId.value.trim();
        const password = this.elements.unlockPassword.value.trim();
        
        if (!deviceId || !password) {
            this.showNotification('Please enter both device ID and password', 'warning');
            return;
        }

        try {
            console.log(`🔓 Attempting to unlock device: ${deviceId}...`);
            
            const response = await fetch(`/api/usb/devices/${deviceId}/unlock`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    password: password,
                    method: 'manual'
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`🎉 ${result.message}`, 'success');
                this.elements.unlockPassword.value = '';
                this.listUSBDevices(); // Refresh device list
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
            this.displayUSBResult(result);
            
        } catch (error) {
            console.error('❌ Failed to unlock device:', error);
            this.showNotification('Failed to unlock device: ' + error.message, 'error');
        }
    }

    displayUSBResult(result) {
        const container = this.elements.usbResultsContent;
        this.elements.usbResults.style.display = 'block';
        
        if (result.success) {
            container.innerHTML = `
                <div class="alert alert-success hacker-card">
                    <h6><i class="fas fa-check-circle"></i> Success!</h6>
                    <p class="mb-0">${result.message}</p>
                    ${result.details ? `
                        <hr>
                        <small>
                            <strong>Device Type:</strong> ${result.details.device_type}<br>
                            <strong>Security Level:</strong> ${result.details.security_level}<br>
                            <strong>Algorithm:</strong> ${result.details.encryption_algorithm}<br>
                            <strong>Attempts:</strong> ${result.details.attempts_made}
                        </small>
                    ` : ''}
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="alert alert-danger hacker-card">
                    <h6><i class="fas fa-exclamation-triangle"></i> Failed</h6>
                    <p class="mb-0">${result.error}</p>
                    ${result.device_locked ? `
                        <hr>
                        <small class="text-warning">
                            <i class="fas fa-lock"></i> Device is temporarily locked
                        </small>
                    ` : ''}
                </div>
            `;
        }
    }

    async getUSBStatistics() {
        try {
            console.log('📊 Fetching USB attack statistics...');
            
            const response = await fetch('/api/usb/statistics');
            const result = await response.json();
            
            if (result.success) {
                this.displayUSBStatistics(result.statistics);
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to get statistics:', error);
            this.showNotification('Failed to get statistics: ' + error.message, 'error');
        }
    }

    displayUSBStatistics(stats) {
        const container = this.elements.usbResultsContent;
        this.elements.usbResults.style.display = 'block';
        
        container.innerHTML = `
            <div class="card hacker-card">
                <div class="card-header">
                    <h6 class="mb-0"><i class="fas fa-chart-bar"></i> Attack Statistics</h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Overall Stats</h6>
                            <p><strong>Total Attempts:</strong> ${stats.total_attempts}</p>
                            <p><strong>Successful:</strong> ${stats.successful_attempts}</p>
                            <p><strong>Failed:</strong> ${stats.failed_attempts}</p>
                            <p><strong>Success Rate:</strong> ${stats.success_rate.toFixed(1)}%</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Method Statistics</h6>
                            ${Object.entries(stats.method_statistics).map(([method, data]) => `
                                <p><strong>${method}:</strong> ${data.successful}/${data.total} (${((data.successful/data.total)*100).toFixed(1)}%)</p>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async resetUSBDevice(deviceId) {
        try {
            console.log(`🔄 Resetting device: ${deviceId}...`);
            
            const response = await fetch(`/api/usb/devices/${deviceId}/reset`, {
                method: 'POST'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ ${result.message}`, 'success');
                this.listUSBDevices(); // Refresh device list
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to reset device:', error);
            this.showNotification('Failed to reset device: ' + error.message, 'error');
        }
    }

    async resetAllUSBDevices() {
        if (!confirm('Are you sure you want to reset all USB devices? This will clear all lockout statuses.')) {
            return;
        }

        try {
            console.log('🔄 Resetting all USB devices...');
            
            // Get all devices and reset them one by one
            const response = await fetch('/api/usb/devices');
            const result = await response.json();
            
            if (result.success) {
                let resetCount = 0;
                for (const device of result.devices) {
                    try {
                        await fetch(`/api/usb/devices/${device.device_id}/reset`, {
                            method: 'POST'
                        });
                        resetCount++;
                    } catch (e) {
                        console.error(`Failed to reset device ${device.device_id}:`, e);
                    }
                }
                
                this.showNotification(`✅ Reset ${resetCount} devices successfully`, 'success');
                this.listUSBDevices(); // Refresh device list
            } else {
                this.showNotification(`❌ ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('❌ Failed to reset devices:', error);
            this.showNotification('Failed to reset devices: ' + error.message, 'error');
        }
    }
}

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new PasswordCrackerApp();
});
