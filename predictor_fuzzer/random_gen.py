import random
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

DEST = '/apollo/modules/prediction/conf/prediction_conf.pb.txt'

evaluator_types = [
    "MLP_EVALUATOR",
    "RNN_EVALUATOR",
    "COST_EVALUATOR",
    "CRUISE_MLP_EVALUATOR",
    "JUNCTION_MLP_EVALUATOR",
    "CYCLIST_KEEP_LANE_EVALUATOR",
    "LANE_SCANNING_EVALUATOR",
    "PEDESTRIAN_INTERACTION_EVALUATOR",
    "JUNCTION_MAP_EVALUATOR",
    "LANE_AGGREGATING_EVALUATOR",
    "SEMANTIC_LSTM_EVALUATOR",
]


def load_template():
    with open(SCRIPT_PATH + '/template', 'r') as f:
        template = f.readlines()

    # positions of arguments in the template
    positions = [15, 22, 29, 36, 47, 53, 64]

    return template, positions


def dump_config(config):
    with open(DEST, 'w') as f:
        f.write(''.join(config))


def random_gen_config():
    template, positions = load_template()

    evaluators = []
    for pos in positions:
        evaluator_str = '  evaluator_type: {}\n'.format(
            random.choice(evaluator_types))
        evaluators.append(evaluator_str)
        template[pos] = evaluator_str

    # print(evaluators)

    return template


def restart_predictor():
    os.system("bash /apollo/scripts/prediction.sh stop")
    os.system("sleep 1")
    os.system("bash /apollo/scripts/prediction.sh start")


def fuzz_config():
    dump_config(random_gen_config())
    restart_predictor()


if __name__ == '__main__':
    fuzz_config()
