<a id="readme-top"></a>
<br />
<h1 align="center">Ethereum Faucet API</h1>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-w sith">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project implements a RESTful API for distributing test Ethereum on the Sepolia testnet. It provides a simple and efficient way for developers to obtain test ETH for their blockchain development needs. The API includes features like transaction tracking, test mode for simulations, and comprehensive error handling.

### Built With

* [![Python][Python.org]][Python-url]
* [![Django][Django.com]][Django-url]
* [![PostgreSQL][Postgresql.org]][Postgresql-url]
* [![Web3.py][Web3.py]][Web3-url]

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to set up the project locally.

### Prerequisites

1. **Python**
   - Version 3.9 or higher
   ```bash
   python --version
   ```

2. **Docker & Docker Compose**
   - Latest stable version
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Infura Account**
   - Create an account at [Infura](https://infura.io)
   - Create a new project and get your Project ID
   - Enable Sepolia testnet

4. **Ethereum Wallet**
   - Create a wallet for the Sepolia testnet
   - Get the wallet address and private key
   - Fund the wallet with Sepolia ETH

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/haseebrehmat/faucet_api.git
   cd faucet_api
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Update the following in your `.env`:
   - INFURA_PROJECT_ID
   - FAUCET_WALLET_PRIVATE_KEY
   - FAUCET_WALLET_ADDRESS
   - Other configuration as needed

3. **Build and start services**
   ```bash
   make build
   make up
   ```

4. **Verify the setup**
   - Open your browser and navigate to `http://localhost:8000/api/`
   - You should see the Django REST framework interface

<p align="right">(<a href="#readme-top">🔝</a>)</p>

<!-- USAGE -->
## Usage

### API Endpoints and Responses

<details>
<summary><strong>1. Fund Wallet</strong></summary>

**Endpoint**: `/api/faucet/fund-wallet/`
**Methods**: GET, POST
**Description**: Sends test ETH to a specified wallet address

#### Request
```bash
curl -X POST http://localhost:8000/api/faucet/fund-wallet/ \
     -H "Content-Type: application/json" \
     -d '{"wallet_address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"}'
```

#### Success Response
```json
{
    "transaction_id": "0x1234...abcd",
    "message": "Transaction sent successfully"
}
```

#### Error Response
```json
{
    "error": "Invalid wallet address format"
}
```
</details>

<details>
<summary><strong>2. Test Transaction</strong></summary>

**Endpoint**: `/api/faucet/test-transaction/`
**Methods**: GET, POST
**Description**: Simulates a transaction without sending funds

#### Request
```bash
curl -X POST http://localhost:8000/api/faucet/test-transaction/ \
     -H "Content-Type: application/json" \
     -d '{"wallet_address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"}'
```

#### Success Response
```json
{
    "transaction_id": "test_tx_0x742d35Cc",
    "message": "Test transaction simulated successfully"
}
```

#### Error Response
```json
{
    "error": "Invalid wallet address format"
}
```
</details>

<details>
<summary><strong>3. Transaction Stats</strong></summary>

**Endpoint**: `/api/faucet/stats/`
**Method**: GET
**Description**: Retrieves transaction statistics

#### Request
```bash
curl http://localhost:8000/api/faucet/stats/
```

#### Success Response
```json
{
    "total_transactions": 100,
    "successful_transactions": 95,
    "failed_transactions": 5,
}
```
</details>

### Docker Commands

- **Build services**: `make build`
- **Start services**: `make up`
- **Start in detached mode**: `make up-d`
- **View logs**: `make logs`
- **Stop services**: `make down`
- **Access shell**: `make shell`
- **Clean up**: `make clean`

<p align="right">(<a href="#readme-top">🔝</a>)</p>

<!-- ROADMAP -->
## Roadmap

**Core Features**
  - Basic API setup
  - Ethereum transaction handling
  - Transaction logging
  - Docker containerization

**Services**
  - **EthereumService**
    - Handles blockchain interactions
    - Manages transaction preparation and sending
    - Supports test mode for simulations
  
  - **StatsService**
    - Tracks transaction statistics
    - Provides analytics endpoints

- **API Views**
  - **FaucetViewSet**
    - Handles all faucet-related operations
    - Provides multiple endpoints for different operations
    - Includes comprehensive error handling

- **Models**
  - **TransactionLog**
    - Records all transaction attempts
    - Stores success/failure status
    - Maintains wallet addresses and transaction IDs
### Architecture Review

<details>
<summary><strong><code>Services</code></strong></summary>

#### `EthereumService`

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `__init__` | Initializes service with Infura and wallet settings | None | None |
| `prepare_transaction` | Prepares ETH transaction | `to_address: str` | `dict` |
| `send_transaction` | Signs and sends transaction | `transaction: dict` | `str` (tx hash) |
| `fund_wallet` | Sends ETH to wallet | `wallet_address: str, test_mode: bool = False` | `dict` |

#### `StatsService`

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get_faucet_stats` | Retrieves transaction statistics | None | `dict` |
| `log_transaction` | Records transaction details | `wallet_address: str, tx_id: str, status: str` | None |

</details>

<details>
<summary><strong><code>API Views</code></strong></summary>

#### `FaucetViewSet`

| Method | Endpoint | Description | Request Method |
|--------|----------|-------------|----------------|
| `fund_wallet` | `/fund-wallet/` | Handles wallet funding | GET, POST |
| `test_transaction` | `/test-transaction/` | Simulates transactions | GET, POST |
| `stats` | `/stats/` | Retrieves statistics | GET |

**Helper Methods**:
- `_handle_get_request`: Handles form views
- `_validate_wallet_address`: Validates addresses
- `_handle_transaction_result`: Processes transaction results

</details>

<details>
<summary><strong><code>Models</code></strong></summary>

#### `TransactionLog`

| Field | Type | Description |
|-------|------|-------------|
| `wallet_address` | CharField | Target wallet address |
| `transaction_id` | CharField | Blockchain transaction ID |
| `status` | CharField | SUCCESS/FAILED/TEST |
| `created_at` | DateTimeField | Transaction timestamp |
| `amount` | DecimalField | ETH amount sent |

**Methods**:
- `__str__`: Returns transaction summary
- `save`: Custom save with amount tracking

</details>


<p align="right">(<a href="#readme-top">🔝</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">🔝</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Django.com]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Postgresql.org]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[Postgresql-url]: https://www.postgresql.org/
[Web3.py]: https://img.shields.io/badge/Web3.py-F16822?style=for-the-badge&logo=ethereum&logoColor=white
[Web3-url]: https://web3py.readthedocs.io/
