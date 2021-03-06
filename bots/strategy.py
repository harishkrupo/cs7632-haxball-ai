"""
 * Copyright 2020 cs7632-haxball-ai team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

from bots.action_chase import Chase
from bots.action_shoot import Shoot
from bots.sequence import Sequence
from bots.selector import Selector
from bots.action_align import Align
from bots.daemon_clearpathtogoal import ClearPathToGoalDaemon
from bots.daemon_sideofthefield import SideOfTheFieldDaemon
from bots.daemon_ball_possession import BallPossession
from bots.daemon_distance_from_opponent import DistanceFromOpponent
from bots.daemon_closest_team_to_ball import ClosestTeamToBall
from bots.daemon_retreat_to_get_possession import RetreatToGetPossession
from bots.action_movetoopponentside import MoveToOpponentSideAction
from bots.action_movebetweenopponentandgoal import MoveBetweenOpponentAndGoal
from bots.action_shoot_at_wall import ShootAtWall
from bots.action_move_towards_opponent_goal import MoveTowardsOpponentGoal
from bots.action_move_close_to_opponent import MoveCloseToOpponent
from bots.action_slightly_deviate import SlightlyDeviate
from bots.action_move_middle_of_self_goal import MoveMiddleOfGoal
from bots.action_face_opponent_goal import FaceOpponentGoal
from bots.daemon_danger_to_goal import DangerToGoal
from bots.action_just_shoot import JustShoot
from bots.action_defender_chase import DefenderChase

import replay

BOT_TEAM = replay.Team.Red
ENEMY_TEAM = replay.Team.Blue

class Strategy():
    def __init__(self):
        # self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner"), (Shoot, "Shooter")]

        self.hybrid_spec = [
            [Selector,
                [(Sequence, "defense_selector"), (BallPossession, "enemy_ball_possession", ENEMY_TEAM, False), (SideOfTheFieldDaemon, False, "side_of_field"), (MoveBetweenOpponentAndGoal, 0.5, "move_between_opponent_and_goal")],
                [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner"), (Shoot, "Shooter")]
            ]
        ]

        self.defend_spec = [
            Selector,
            [
                Sequence,
                (DangerToGoal, 165, "danger_to_goal"),
                (DefenderChase, 165, "chase"),
                (Shoot, "shoot"),
                (MoveMiddleOfGoal, "move_middle_of_goal")

            ],
            [
                Sequence,
                (MoveBetweenOpponentAndGoal, 0.75, "move_between_opponent_and_goal"),
                (JustShoot, "Shooter")
            ]
        ]

        self.attack_spec = [
            (Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner"), (Shoot, "Shooter")
        ]

        # self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner")]
        # self.spec = [(Chase, "Chaser")]
        # self.spec = [MoveToOpponentSideAction] [(MoveBetweenOpponentAndGoal, 0.75)] [MoveToOpponentSideAction] [SideOfTheFieldDaemon] [ClearPathToGoalDaemon] -- EXAMPLE ONLY
        # self.spec = [Selector,
        #     [(BallPossession, "our_ball_possession", BOT_TEAM, True),
        #         [Selector,
        #             [ClearPathToGoalDaemon,
        #                 [Selector,
        #                     [SideOfTheFieldDaemon,
        #                         [Sequence,
        #                             [Align, Shoot]
        #                         ]
        #                     ]
        #                 ],
        #                 MoveToOpponentSideAction
        #             ],
        #             [Selector,
        #                 [(DistanceFromOpponent, "shoot_at_wall_daemon", BOT_TEAM, 100), ShootAtWall],
        #                 [Sequence, Align, MoveTowardsOpponentGoal]
        #             ]
        #         ]
        #     ],
        #     [Selector,
        #         [(BallPossession, "enemy_ball_possession", ENEMY_TEAM, False),
        #             [Selector,
        #                 [SideOfTheFieldDaemon, (MoveBetweenOpponentAndGoal, 0.75)],
        #                 [Sequence, MoveCloseToOpponent, SlightlyDeviate, Chase]
        #             ]
        #         ],
        #         [Selector,
        #             [(ClosestTeamToBall, "we_are_close", BOT_TEAM),
        #                 [Selector,
        #                     [RetreatToGetPossession, MoveMiddleOfGoal], Chase
        #                 ]
        #             ],
        #             [Selector,
        #                 [(DistanceFromOpponent, "distance", BOT_TEAM, 100),
        #                     [Selector,
        #                         [RetreatToGetPossession,
        #                             [Sequence, Chase, ShootAtWall]
        #                         ],
        #                         [Sequence, Chase, Shoot]
        #                     ]
        #                 ],
        #                 [Sequence, Chase, FaceOpponentGoal]
        #             ]
        #         ]
        #     ]
        # ]

    def getHybridStrategy(self):
        return self.hybrid_spec

    def getDefendStrategy(self):
        return self.defend_spec

    def getAttackStrategy(self):
        return self.attack_spec
