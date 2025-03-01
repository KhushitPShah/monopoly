<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monopoly Transactor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --primary-color: #5D5CDE;
            --secondary-color: #34D399;
            --error-color: #EF4444;
            --success-color: #10B981;
        }

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #181818;
                --text-color: #FFFFFF;
                --card-bg: #2D2D2D;
                --button-hover: #4D4CB8;
            }
        }

        @media (prefers-color-scheme: light) {
            :root {
                --bg-color: #FFFFFF;
                --text-color: #181818;
                --card-bg: #F3F4F6;
                --button-hover: #4D4CB8;
            }
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
            transition: background-color 0.3s, color 0.3s;
        }

        .card {
            background-color: var(--card-bg);
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }

        .btn {
            transition: background-color 0.2s, transform 0.1s;
        }

        .btn:hover {
            background-color: var(--button-hover);
        }

        .btn:active {
            transform: scale(0.98);
        }

        .numpad-btn {
            width: 3.5rem;
            height: 3.5rem;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.5rem;
            background-color: var(--card-bg);
            color: var(--text-color);
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
        }

        .numpad-btn:hover {
            background-color: var(--button-hover);
            color: white;
        }

        .numpad-btn:active {
            transform: scale(0.95);
        }

        .loader {
            border: 3px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 3px solid var(--primary-color);
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .fade-in {
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        .shake {
            animation: shake 0.5s ease-in-out;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8">
    <div class="container mx-auto max-w-2xl">
        <!-- Header -->
        <div class="text-center mb-6">
            <h1 class="text-3xl md:text-4xl font-bold mb-2">Monopoly Transactor</h1>
            <p class="text-sm md:text-base opacity-75" id="version">v1.0 - RFID Simulation</p>
        </div>

        <!-- Status Display -->
        <div class="card p-4 md:p-6 mb-6 text-center">
            <h2 class="text-xl font-semibold mb-2" id="mode-display">Mode: Idle</h2>
            <div class="text-3xl md:text-4xl font-bold my-3" id="balance-display">Balance: -</div>
            <div class="text-md md:text-lg my-2" id="message-display">Tap a card to begin</div>
        </div>

        <!-- Card Simulation Buttons -->
        <div class="grid grid-cols-2 gap-4 mb-6">
            <button id="card1-btn" class="card p-4 py-5 text-center btn bg-primary-100 hover:bg-primary-200 active:bg-primary-300" style="background-color: var(--primary-color); color: white;">
                Simulate Card 1
            </button>
            <button id="card2-btn" class="card p-4 py-5 text-center btn bg-secondary-100 hover:bg-secondary-200 active:bg-secondary-300" style="background-color: var(--secondary-color); color: white;">
                Simulate Card 2
            </button>
        </div>

        <!-- Mode Buttons -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            <button id="transfer-btn" class="card p-3 md:p-4 text-center btn hover:bg-gray-200 dark:hover:bg-gray-700">
                Transfer
            </button>
            <button id="bidding-btn" class="card p-3 md:p-4 text-center btn hover:bg-gray-200 dark:hover:bg-gray-700">
                Bidding
            </button>
            <button id="loan-btn" class="card p-3 md:p-4 text-center btn hover:bg-gray-200 dark:hover:bg-gray-700">
                Loan
            </button>
            <button id="repay-btn" class="card p-3 md:p-4 text-center btn hover:bg-gray-200 dark:hover:bg-gray-700">
                Repay
            </button>
        </div>

        <!-- Input Area (Initially Hidden) -->
        <div id="input-area" class="mb-6 hidden fade-in">
            <!-- Keypad Input -->
            <div id="keypad-container" class="card p-4 md:p-6">
                <div class="bg-gray-100 dark:bg-gray-800 p-3 rounded mb-4 text-right text-2xl md:text-3xl font-mono" id="amount-display">0</div>
                
                <div class="grid grid-cols-3 gap-2 mb-3">
                    <div class="numpad-btn">1</div>
                    <div class="numpad-btn">2</div>
                    <div class="numpad-btn">3</div>
                    <div class="numpad-btn">4</div>
                    <div class="numpad-btn">5</div>
                    <div class="numpad-btn">6</div>
                    <div class="numpad-btn">7</div>
                    <div class="numpad-btn">8</div>
                    <div class="numpad-btn">9</div>
                    <div class="numpad-btn">0</div>
                    <div class="numpad-btn">00</div>
                    <div class="numpad-btn">000</div>
                </div>

                <div class="flex gap-2">
                    <button id="clear-btn" class="flex-1 py-3 bg-red-500 text-white rounded hover:bg-red-600 active:bg-red-700">Clear</button>
                    <button id="backspace-btn" class="py-3 px-4 bg-gray-300 dark:bg-gray-700 rounded hover:bg-gray-400 dark:hover:bg-gray-600">⌫</button>
                    <button id="confirm-amount-btn" class="flex-1 py-3 bg-green-500 text-white rounded hover:bg-green-600 active:bg-green-700">Confirm</button>
                </div>
            </div>

            <!-- Bidding Controls -->
            <div id="bidding-container" class="card p-4 md:p-6 hidden">
                <div class="text-2xl font-bold text-center mb-4" id="current-bid-display">Current Bid: $0</div>
                
                <div class="grid grid-cols-3 gap-2 mb-4">
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="100">+$100</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="500">+$500</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="1000">+$1K</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="5000">+$5K</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="10000">+$10K</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="50000">+$50K</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="100000">+$100K</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="500000">+$500K</button>
                    <button class="bid-increment p-2 bg-blue-100 dark:bg-blue-900 rounded hover:bg-blue-200 dark:hover:bg-blue-800" data-value="1000000">+$1M</button>
                </div>

                <div class="flex gap-2">
                    <button id="reset-bid-btn" class="flex-1 py-3 bg-gray-300 dark:bg-gray-700 rounded hover:bg-gray-400 dark:hover:bg-gray-600">Reset</button>
                    <button id="confirm-bid-btn" class="flex-1 py-3 bg-green-500 text-white rounded hover:bg-green-600 active:bg-green-700">Confirm Bid</button>
                </div>
            </div>
        </div>

        <!-- Reset Button -->
        <div class="text-center mb-6">
            <button id="reset-btn" class="px-4 py-2 rounded text-white" style="background-color: var(--primary-color);">
                Reset
            </button>
        </div>

        <!-- Notification -->
        <div id="notification" class="fixed bottom-4 right-4 p-4 rounded-lg shadow-lg hidden bg-green-500 text-white">
            Operation successful!
        </div>
    </div>

    <script>
        // Card Data Management
        const DEFAULT_BALANCE = 1500000; // 1.5M
        let cards = {};
        
        // Initialize or load saved data
        function initializeCardData() {
            const savedData = localStorage.getItem('monopolyCards');
            if (savedData) {
                try {
                    cards = JSON.parse(savedData);
                } catch (e) {
                    console.error("Error loading card data:", e);
                    resetCardData();
                }
            } else {
                resetCardData();
            }
        }
        
        function resetCardData() {
            cards = {
                "card1": {
                    balance: DEFAULT_BALANCE,
                    transactions: 0,
                    loans: []
                },
                "card2": {
                    balance: DEFAULT_BALANCE,
                    transactions: 0,
                    loans: []
                }
            };
            saveCardData();
        }
        
        function saveCardData() {
            try {
                localStorage.setItem('monopolyCards', JSON.stringify(cards));
            } catch (e) {
                console.error("Error saving card data:", e);
                showNotification("Error saving data", "error");
            }
        }
        
        // App State
        let currentMode = "idle";
        let currentCard = null;
        let senderCard = null;
        let receiverCard = null;
        let amount = 0;
        let baseBid = 0;
        let currentBid = 0;
        
        // UI Element References
        const modeDisplay = document.getElementById('mode-display');
        const balanceDisplay = document.getElementById('balance-display');
        const messageDisplay = document.getElementById('message-display');
        const amountDisplay = document.getElementById('amount-display');
        const currentBidDisplay = document.getElementById('current-bid-display');
        const inputArea = document.getElementById('input-area');
        const keypadContainer = document.getElementById('keypad-container');
        const biddingContainer = document.getElementById('bidding-container');
        const notification = document.getElementById('notification');
        
        // Format Currency Functions
        function formatAmount(amount) {
            if (amount >= 1000000) {
                return `$${(amount/1000000).toFixed(2).replace(/\.00$/, '')}M`;
            } else if (amount >= 1000) {
                return `$${(amount/1000).toFixed(2).replace(/\.00$/, '')}K`;
            } else {
                return `$${amount}`;
            }
        }
        
        function formatDisplayAmount(amountStr) {
            // Format for display in the amount input
            if (!amountStr || amountStr === '0') return '0';
            
            const num = parseInt(amountStr.replace(/,/g, ''));
            return num.toLocaleString();
        }
        
        // UI Update Functions
        function updateModeDisplay(mode) {
            modeDisplay.textContent = `Mode: ${mode.charAt(0).toUpperCase() + mode.slice(1)}`;
        }
        
        function updateBalanceDisplay(balance) {
            balanceDisplay.textContent = balance ? `Balance: ${formatAmount(balance)}` : 'Balance: -';
        }
        
        function updateMessageDisplay(message) {
            messageDisplay.textContent = message;
        }
        
        function showInputArea(type = 'keypad') {
            inputArea.classList.remove('hidden');
            
            if (type === 'keypad') {
                keypadContainer.classList.remove('hidden');
                biddingContainer.classList.add('hidden');
                amountDisplay.textContent = '0';
            } else if (type === 'bidding') {
                keypadContainer.classList.add('hidden');
                biddingContainer.classList.remove('hidden');
                currentBidDisplay.textContent = `Current Bid: ${formatAmount(currentBid)}`;
            }
        }
        
        function hideInputArea() {
            inputArea.classList.add('hidden');
        }
        
        function showNotification(message, type = 'success') {
            notification.textContent = message;
            
            if (type === 'error') {
                notification.classList.remove('bg-green-500');
                notification.classList.add('bg-red-500');
            } else {
                notification.classList.remove('bg-red-500');
                notification.classList.add('bg-green-500');
            }
            
            notification.classList.remove('hidden');
            
            setTimeout(() => {
                notification.classList.add('hidden');
            }, 3000);
        }
        
        // Card Interaction Functions
        function simulateCardTap(cardId) {
            currentCard = cardId;
            
            switch(currentMode) {
                case 'idle':
                    displayCardInfo(cardId);
                    break;
                case 'transfer_sender':
                    senderCard = cardId;
                    displayCardInfo(cardId);
                    updateMessageDisplay('Enter amount to transfer');
                    currentMode = 'transfer_amount';
                    showInputArea('keypad');
                    break;
                case 'transfer_receiver':
                    receiverCard = cardId;
                    processTransfer();
                    break;
                case 'bidding_card':
                    displayCardInfo(cardId);
                    updateMessageDisplay('Enter base bid amount');
                    currentMode = 'bidding_base';
                    showInputArea('keypad');
                    break;
                case 'bidding_final':
                    processBid(cardId);
                    break;
                case 'loan_card':
                    displayCardInfo(cardId);
                    updateMessageDisplay('Enter loan amount');
                    currentMode = 'loan_amount';
                    showInputArea('keypad');
                    break;
                case 'repay_card':
                    processRepayment(cardId);
                    break;
            }
        }
        
        function displayCardInfo(cardId) {
            const card = cards[cardId];
            updateBalanceDisplay(card.balance);
            
            if (card.transactions > 0) {
                updateMessageDisplay(`Please repay ${card.transactions}`);
            } else {
                updateMessageDisplay(`Card ${cardId.slice(-1)} - Ready`);
            }
        }
        
        // Process Functions
        function processTransfer() {
            if (senderCard === receiverCard) {
                updateMessageDisplay('Cannot transfer to the same card');
                showNotification('Cannot transfer to the same card', 'error');
                return;
            }
            
            try {
                // Check for sufficient funds
                if (amount > cards[senderCard].balance) {
                    updateMessageDisplay('Insufficient funds for transfer');
                    showNotification('Insufficient funds', 'error');
                    return;
                }
                
                // Perform the transfer
                cards[senderCard].balance -= amount;
                cards[receiverCard].balance += amount;
                
                // Update display
                displayCardInfo(receiverCard);
                
                // Show notification
                const amountStr = formatAmount(amount);
                showNotification(`Transferred ${amountStr} successfully`);
                updateMessageDisplay(`Transferred ${amountStr} from Card ${senderCard.slice(-1)} to Card ${receiverCard.slice(-1)}`);
                
                // Save data
                saveCardData();
                
                // Reset after delay
                setTimeout(resetToIdle, 3000);
                
            } catch (error) {
                console.error("Transfer error:", error);
                updateMessageDisplay('Error processing transfer');
                showNotification('Error processing transfer', 'error');
            }
        }
        
        function processBid(cardId) {
            try {
                // Check for sufficient funds
                if (currentBid > cards[cardId].balance) {
                    updateMessageDisplay('Insufficient funds for bid');
                    showNotification('Insufficient funds', 'error');
                    return;
                }
                
                // Deduct bid amount
                cards[cardId].balance -= currentBid;
                
                // Increment transactions counter
                cards[cardId].transactions += 1;
                
                // Update display
                displayCardInfo(cardId);
                
                // Show notification
                const bidStr = formatAmount(currentBid);
                showNotification(`Bid of ${bidStr} paid successfully`);
                
                // Save data
                saveCardData();
                
                // Reset after delay
                setTimeout(resetToIdle, 3000);
                
            } catch (error) {
                console.error("Bid error:", error);
                updateMessageDisplay('Error processing bid');
                showNotification('Error processing bid', 'error');
            }
        }
        
        function processLoan() {
            try {
                // Add loan amount to card
                cards[currentCard].balance += amount;
                
                // Store loan information
                cards[currentCard].loans.push({
                    amount: amount,
                    paid: false,
                    timestamp: Date.now()
                });
                
                // Update display
                displayCardInfo(currentCard);
                
                // Show notification
                const amountStr = formatAmount(amount);
                showNotification(`Loan of ${amountStr} added successfully`);
                updateMessageDisplay(`Loan of ${amountStr} added to Card ${currentCard.slice(-1)}`);
                
                // Save data
                saveCardData();
                
                // Reset after delay
                setTimeout(resetToIdle, 3000);
                
            } catch (error) {
                console.error("Loan error:", error);
                updateMessageDisplay('Error processing loan');
                showNotification('Error processing loan', 'error');
            }
        }
        
        function processRepayment(cardId) {
            try {
                const card = cards[cardId];
                const transactions = card.transactions;
                
                if (transactions === 0) {
                    updateMessageDisplay('No loans to repay');
                    showNotification('No loans to repay', 'error');
                    return;
                }
                
                // Calculate interest (5% base + 1% per transaction after the first)
                let interestRate = 0.05;
                if (transactions > 1) {
                    interestRate += (transactions - 1) * 0.01;
                }
                
                // Find unpaid loans
                const unpaidLoans = card.loans.filter(loan => !loan.paid);
                
                if (unpaidLoans.length === 0) {
                    updateMessageDisplay('No unpaid loans found');
                    showNotification('No unpaid loans found', 'error');
                    return;
                }
                
                // Calculate total repayment
                const loanTotal = unpaidLoans.reduce((sum, loan) => sum + loan.amount, 0);
                const interestAmount = Math.round(loanTotal * interestRate);
                const totalRepayment = loanTotal + interestAmount;
                
                // Check for sufficient funds
                if (totalRepayment > card.balance) {
                    updateMessageDisplay('Insufficient funds to repay loans');
                    showNotification('Insufficient funds', 'error');
                    return;
                }
                
                // Process repayment
                card.balance -= totalRepayment;
                
                // Mark loans as paid
                unpaidLoans.forEach(loan => {
                    loan.paid = true;
                    loan.repaidTimestamp = Date.now();
                });
                
                // Reset transaction counter
                card.transactions = 0;
                
                // Update display
                displayCardInfo(cardId);
                
                // Show notification
                const repaymentStr = formatAmount(totalRepayment);
                const interestStr = formatAmount(interestAmount);
                showNotification(`Repayment successful`);
                updateMessageDisplay(`Repaid ${repaymentStr} (incl. ${interestStr} interest)`);
                
                // Save data
                saveCardData();
                
                // Reset after delay
                setTimeout(resetToIdle, 3000);
                
            } catch (error) {
                console.error("Repayment error:", error);
                updateMessageDisplay('Error processing repayment');
                showNotification('Error processing repayment', 'error');
            }
        }
        
        // Mode Functions
        function startTransferMode() {
            resetToIdle();
            currentMode = 'transfer_sender';
            updateModeDisplay('Transfer');
            updateMessageDisplay('Tap sender\'s card');
        }
        
        function startBiddingMode() {
            resetToIdle();
            currentMode = 'bidding_card';
            updateModeDisplay('Bidding');
            updateMessageDisplay('Tap card of bidder');
        }
        
        function startLoanMode() {
            resetToIdle();
            currentMode = 'loan_card';
            updateModeDisplay('Loan');
            updateMessageDisplay('Tap card to receive loan');
        }
        
        function startRepayMode() {
            resetToIdle();
            currentMode = 'repay_card';
            updateModeDisplay('Repay');
            updateMessageDisplay('Tap card to repay loan');
        }
        
        function resetToIdle() {
            currentMode = 'idle';
            updateModeDisplay('Idle');
            updateBalanceDisplay(null);
            updateMessageDisplay('Tap a card to begin');
            hideInputArea();
            
            // Reset variables
            currentCard = null;
            senderCard = null;
            receiverCard = null;
            amount = 0;
            baseBid = 0;
            currentBid = 0;
        }
        
        // Amount Input Functions
        function handleNumpadInput(value) {
            const currentAmount = amountDisplay.textContent.replace(/,/g, '');
            
            // Prevent adding too many digits
            if (currentAmount.length >= 9 && currentAmount !== '0') {
                return;
            }
            
            let newAmount;
            if (currentAmount === '0') {
                newAmount = value;
            } else {
                newAmount = currentAmount + value;
            }
            
            amountDisplay.textContent = formatDisplayAmount(newAmount);
        }
        
        function clearAmount() {
            amountDisplay.textContent = '0';
        }
        
        function backspaceAmount() {
            const currentAmount = amountDisplay.textContent.replace(/,/g, '');
            if (currentAmount.length <= 1) {
                amountDisplay.textContent = '0';
            } else {
                const newAmount = currentAmount.slice(0, -1);
                amountDisplay.textContent = formatDisplayAmount(newAmount);
            }
        }
        
        function confirmAmount() {
            try {
                const enteredAmount = parseInt(amountDisplay.textContent.replace(/,/g, ''));
                
                if (isNaN(enteredAmount) || enteredAmount <= 0) {
                    updateMessageDisplay('Please enter a valid amount');
                    messageDisplay.classList.add('shake');
                    setTimeout(() => {
                        messageDisplay.classList.remove('shake');
                    }, 500);
                    return;
                }
                
                amount = enteredAmount;
                
                switch (currentMode) {
                    case 'transfer_amount':
                        // Check if sender has enough funds
                        if (amount > cards[senderCard].balance) {
                            updateMessageDisplay('Insufficient funds');
                            showNotification('Insufficient funds', 'error');
                            return;
                        }
                        
                        updateMessageDisplay('Tap receiver\'s card');
                        currentMode = 'transfer_receiver';
                        hideInputArea();
                        break;
                        
                    case 'bidding_base':
                        baseBid = amount;
                        currentBid = amount;
                        updateMessageDisplay('Adjust bid with increments');
                        currentMode = 'bidding_increment';
                        showInputArea('bidding');
                        break;
                        
                    case 'loan_amount':
                        processLoan();
                        hideInputArea();
                        break;
                }
                
            } catch (error) {
                console.error("Amount input error:", error);
                updateMessageDisplay('Invalid amount');
                showNotification('Invalid amount', 'error');
            }
        }
        
        // Bidding Functions
        function addToBid(increment) {
            currentBid += increment;
            currentBidDisplay.textContent = `Current Bid: ${formatAmount(currentBid)}`;
        }
        
        function resetBid() {
            currentBid = baseBid;
            currentBidDisplay.textContent = `Current Bid: ${formatAmount(baseBid)}`;
        }
        
        function confirmBid() {
            updateMessageDisplay('Tap card to confirm and pay bid');
            currentMode = 'bidding_final';
            hideInputArea();
        }
        
        // Event Listeners
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize data
            initializeCardData();
            
            // Card simulation buttons
            document.getElementById('card1-btn').addEventListener('click', () => simulateCardTap('card1'));
            document.getElementById('card2-btn').addEventListener('click', () => simulateCardTap('card2'));
            
            // Mode buttons
            document.getElementById('transfer-btn').addEventListener('click', startTransferMode);
            document.getElementById('bidding-btn').addEventListener('click', startBiddingMode);
            document.getElementById('loan-btn').addEventListener('click', startLoanMode);
            document.getElementById('repay-btn').addEventListener('click', startRepayMode);
            document.getElementById('reset-btn').addEventListener('click', resetToIdle);
            
            // Keypad buttons
            const numpadButtons = document.querySelectorAll('.numpad-btn');
            numpadButtons.forEach(button => {
                button.addEventListener('click', () => handleNumpadInput(button.textContent));
            });
            
            document.getElementById('clear-btn').addEventListener('click', clearAmount);
            document.getElementById('backspace-btn').addEventListener('click', backspaceAmount);
            document.getElementById('confirm-amount-btn').addEventListener('click', confirmAmount);
            
            // Bidding buttons
            const bidIncrementButtons = document.querySelectorAll('.bid-increment');
            bidIncrementButtons.forEach(button => {
                button.addEventListener('click', () => addToBid(parseInt(button.getAttribute('data-value'))));
            });
            
            document.getElementById('reset-bid-btn').addEventListener('click', resetBid);
            document.getElementById('confirm-bid-btn').addEventListener('click', confirmBid);
        });
    </script>
</body>
</html>
