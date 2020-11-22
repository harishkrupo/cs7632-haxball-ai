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

import replay

BOT_TEAM = replay.Team.Red
ENEMY_TEAM = replay.Team.Blue

class Strategy():
    def __init__(self):
        self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner"), (Shoot, "Shooter")]
        # self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner")]
        # self.spec = [(Chase, "Chaser")]
        # self.spec = [MoveToOpponentSideAction] [(MoveBetweenOpponentAndGoal, 0.75)] [MoveToOpponentSideAction] [SideOfTheFieldDaemon] [ClearPathToGoalDaemon] -- EXAMPLE ONLY
        self.spec = [
            Selector,
            [
                Sequence,
                (BallPossession, "g1 Our ball possession", BOT_TEAM, True),
                [
                    (ClearPathToGoalDaemon, "g2 Clear path to goal"),
                    [
                        (SideOfTheFieldDaemon, "g3 Side of the field daemon"),
                        [
                            Sequence,
                            [
                                (Align, "g4 Align"),
                                (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot")
                            ]
                        ],
                        (MoveToOpponentSideAction, "g6 Move to opponent side action")
                    ],
                    [
                        Selector,
                        [
                            Sequence,
                            (DistanceFromOpponent, "g7 Shoot at wall daemon", BOT_TEAM, 100),
                            (ShootAtWall, "g8 Shoot at wall")
                        ],
                        [
                            Sequence,
                            (Align, "g9 Align"),
                            (MoveTowardsOpponentGoal, "g10 Move towards opponent goal")
                        ]
                    ]
                ]
            ],
            [
                Selector,
                [
                    Sequence,
                    (BallPossession, "g11 Enemy ball possession", ENEMY_TEAM, False),
                    [
                        Selector,
                        [
                            Sequence,
                            (SideOfTheFieldDaemon, "g12 Side of the field daemon"),
                            (MoveBetweenOpponentAndGoal, "g13 Move between opponent and goal", 0.75)
                        ],
                        [
                            Sequence,
                            (MoveCloseToOpponent, "g14 Move close to opponent"),
                            (SlightlyDeviate, "g15 Slightly deviate"),
                            (Chase, "g16 Chase")
                        ]
                    ]
                ],
                [
                    Selector,
                    [
                        Sequence,
                        (ClosestTeamToBall, "g17 Closest team to ball is us", BOT_TEAM),
                        [
                            Selector,
                            [
                                Sequence,
                                (RetreatToGetPossession, "g18 Retreat to get possession"),
                                (MoveMiddleOfGoal, "g19 Move middle of the goal")
                            ],
                            [
                                Sequence,
                                (Chase, "g20 Chase"),
                                (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot"),
                                # (Shoot, "g5 Shoot")
                            ]
                        ]
                    ],
                    [
                        Selector,
                        [
                            Sequence,
                            (DistanceFromOpponent, "g21 Distance from opponent", BOT_TEAM, 100),
                            [
                                Selector,
                                [
                                    Sequence,
                                    (RetreatToGetPossession, "g22 Retreat to get possession"),
                                    [
                                        Sequence,
                                        (Chase, "g23 Chase"),
                                        (ShootAtWall, "g24 Shoot at wall")
                                    ]
                                ],
                                [
                                    Sequence,
                                    (Chase, "g25 Chase"),
                                    (Shoot, "g5 Shoot"),
                                    # (Shoot, "g5 Shoot"),
                                    # (Shoot, "g5 Shoot"),
                                    # (Shoot, "g5 Shoot"),
                                    # (Shoot, "g5 Shoot")
                                ]
                            ]
                        ],
                        [
                            Sequence,
                            (Chase, "g27 Chase"),
                            (FaceOpponentGoal, "g28 Face Opponent Goal"),
                            (Shoot, "g5 Shoot"),
                            # (Shoot, "g5 Shoot"),
                            # (Shoot, "g5 Shoot"),
                            # (Shoot, "g5 Shoot"),
                            # (Shoot, "g5 Shoot")
                        ]
                    ]
                ]
            ]
        ]

    def getStrategy(self):
        return self.spec
