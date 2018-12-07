# -*- coding: utf-8 -*-
import pytest

from ...types import DistanceHypothesis, GaussianStatePrediction,\
    GaussianMeasurementPrediction
from ...hypothesiser.probability import PDAHypothesiser


@pytest.fixture()
def hypothesiser():
    class TestGaussianHypothesiser:
        def hypothesise(self, track, detections, timestamp):
            hypotheses = list()
            for detection in detections:
                prediction = GaussianStatePrediction(track.state_vector + 1,
                                                     track.covar * 2,
                                                     detection.timestamp)
                measurement_prediction =\
                    GaussianMeasurementPrediction(prediction.state_vector,
                                                  prediction.covar,
                                                  prediction.timestamp)
                distance = abs(track.state_vector - detection.state_vector)

                hypotheses.append(DistanceHypothesis(
                    prediction, detection, distance, measurement_prediction))

            prediction = GaussianStatePrediction(track.state_vector + 1,
                                                 track.covar * 2, timestamp)
            hypotheses.append(DistanceHypothesis(prediction, None, 10))
            return hypotheses
    return TestGaussianHypothesiser()


def proabability_predictor():
    class TestGaussianPredictor:
        def predict(self, prior, control_input=None, timestamp=None, **kwargs):
            return GaussianStatePrediction(prior.state_vector + 1,
                                           prior.covar * 2, timestamp)
    return TestGaussianPredictor()


def proabability_updater():
    class TestGaussianUpdater:
        def get_measurement_prediction(self, state_prediction, **kwargs):
            return GaussianMeasurementPrediction(state_prediction.state_vector,
                                                 state_prediction.covar,
                                                 state_prediction.timestamp)
    return TestGaussianUpdater()


@pytest.fixture()
def proabability_hypothesiser():

    return PDAHypothesiser(proabability_predictor(), proabability_updater(),
                           clutter_spatial_density=1.2e-2,
                           prob_detect=0.9, prob_gate=0.99)
