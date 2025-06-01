# SCARA - Smart Contract Adaptive Reasoning Architecture

SCARA is an advanced system for autonomous smart contract evolution, combining AI-driven mutations, on-chain governance, and narrative generation.

## Features

- **Logic Mutation System**: Autonomous contract optimization and evolution
- **AI Co-Agents**: Alith (dream seed generation) and Hyperion (reasoning)
- **Mutation DAO**: On-chain governance for mutation decisions
- **Lore Engine**: Narrative generation based on contract events
- **Mutation Sandbox**: Safe testing environment for mutations
- **Visualization**: DNA sequence and logic tree visualization

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SCARA.git
cd SCARA
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
ETHEREUM_RPC_URL=http://localhost:8545
TEST_ADDRESS=your_test_address
DAO_CONTRACT_ADDRESS=your_dao_contract_address
OPENAI_API_KEY=your_openai_api_key
```

## Running Tests

To verify all components are working:

```bash
python scripts/test_system.py
```

This will test:
- Logic mutation system
- AI mutation system
- Mutation DAO
- Lore engine
- Onchain mutation system
- Mutation sandbox

## Project Structure

```
SCARA/
├── core/
│   └── contracts/
│       ├── logic_mutation.py
│       ├── ai_mutation.py
│       ├── mutation_dao.py
│       ├── lore_engine.py
│       ├── onchain_mutation.py
│       └── mutation_sandbox.py
├── scripts/
│   └── test_system.py
├── contracts/
│   └── MutableCounter.sol
├── frontend/
│   └── src/
│       ├── components/
│       └── hooks/
├── requirements.txt
└── README.md
```

## Usage

1. **Logic Mutation**:
```python
from core.contracts.logic_mutation import LogicMutator

mutator = LogicMutator(
    performance_thresholds={...},
    mutation_rules={...}
)
mutation = await mutator.generate_mutation(context)
```

2. **AI Co-Agents**:
```python
from core.contracts.ai_mutation import AIMutationManager

ai_manager = AIMutationManager()
dream_seed = await ai_manager.alith.generate_dream_seed()
proposal = await ai_manager.propose_mutation(dream_seed, "Description")
```

3. **Mutation DAO**:
```python
from core.contracts.mutation_dao import MutationDAO

dao = MutationDAO(web3, contract_address)
proposal_id = await dao.propose_mutation(mutation_id, description, proposer)
```

4. **Lore Engine**:
```python
from core.contracts.lore_engine import LoreEngine

lore = LoreEngine(narrative_style="epic")
lore.add_event(event)
entries = lore.get_lore_entries(event_type="MutationApplied")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 