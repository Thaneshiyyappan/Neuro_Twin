import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export class AvatarController {
    constructor(scene) {
        this.scene = scene;
        this.avatarGroup = new THREE.Group();
        this.scene.add(this.avatarGroup);

        this.mixer = null;
        this.headBone = null;
        this.morphMesh = null;
        this.isSpeaking = false;
        this.lookTarget = new THREE.Vector3(0, 4, 20);
    }

    async loadAvatar(url = '/assets/models/thanesh_avatar.glb') {
        const loader = new GLTFLoader();
        return new Promise((resolve) => {
            loader.load(
                url,
                (gltf) => {
                    const model = gltf.scene;
                    model.scale.set(2.2, 2.2, 2.2);
                    model.position.set(0, 0.4, 0);

                    model.traverse((child) => {
                        if (child.isBone && /head|neck/i.test(child.name) && !this.headBone) {
                            this.headBone = child;
                        }
                        if (child.isMesh && child.morphTargetDictionary) {
                            this.morphMesh = child;
                        }
                    });

                    if (gltf.animations && gltf.animations.length > 0) {
                        this.mixer = new THREE.AnimationMixer(model);
                        this.mixer.clipAction(gltf.animations[0]).play();
                    }

                    this.avatarGroup.add(model);
                    resolve(true);
                },
                undefined,
                () => {
                    console.warn('Custom .glb not found yet — keeping procedural holographic avatar active.');
                    resolve(false);
                }
            );
        });
    }

    update(delta, elapsedTime) {
        if (this.mixer) this.mixer.update(delta);

        if (this.headBone) {
            const angleY = Math.atan2(this.lookTarget.x, this.lookTarget.z);
            this.headBone.rotation.y = THREE.MathUtils.lerp(this.headBone.rotation.y, angleY * 0.4, 0.08);
        }

        if (this.morphMesh) {
            const dict = this.morphMesh.morphTargetDictionary;
            const idx = dict['mouthOpen'] ?? dict['viseme_aa'] ?? 0;
            const targetVal = this.isSpeaking ? Math.abs(Math.sin(elapsedTime * 16)) * 0.75 : 0;
            this.morphMesh.morphTargetInfluences[idx] = THREE.MathUtils.lerp(
                this.morphMesh.morphTargetInfluences[idx] || 0,
                targetVal,
                0.2
            );
        }
    }
}