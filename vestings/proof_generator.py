import sqlalchemy.orm as orm
from database import VestingModel, ProofModel
import merkle_proof


def generate_and_add_proof(db: orm.Session, type):

    vestings = db.query(VestingModel).filter(VestingModel.type == type)
    vesting_ids = list(map(lambda vesting: vesting.vesting_id, vestings))

    for vesting in vestings:

        proof, root = merkle_proof.generate(vesting_ids, vesting.vesting_id)

        proof_index = 0
        for part in proof:

            proof_model = ProofModel(
                vesting_id=vesting.vesting_id,
                proof_index=proof_index,
                proof=part
            )

            db.add(proof_model)
            db.commit()
            db.refresh(proof_model)

            proof_index += 1